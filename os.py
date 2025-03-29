import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import pandas as pd
from collections import deque

# ---------------------------
# Custom CSS for Enhanced Styling
# ---------------------------
st.markdown("""
    <style>
    /* Overall background and font styling */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f5f5f5;
    }
    .reportview-container {
        background-color: #f5f5f5;
    }
    .sidebar .sidebar-content {
        background-color: #e0e0e0;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5em 1em;
        font-size: 1em;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# App Configuration
# ---------------------------
st.set_page_config(page_title="Virtual Memory Simulator", layout="wide")
st.title("Virtual Memory Simulator")
st.markdown("""
This simulator demonstrates two key aspects of virtual memory management:
- **Page Replacement Simulation:** Visualize page replacement using LRU and Optimal algorithms.
- **Memory Fragmentation Simulation:** See how dynamic allocation and deallocation affect memory fragmentation.
""")

# Sidebar: Select Simulation Type
sim_type = st.sidebar.selectbox("Choose Simulation", 
                                  ["Page Replacement Simulation", "Memory Fragmentation Simulation"])

# ===========================
# Page Replacement Simulation
# ===========================
def simulate_page_replacement(page_refs, num_frames, algorithm="LRU"):
    frames = [-1] * num_frames
    page_faults = 0
    frame_history = []  # Snapshot of frames at each step
    fault_markers = []  # Marks if a page fault occurred at that step
    recency = deque()   # For LRU tracking

    for i, page in enumerate(page_refs):
        fault = False
        if page in frames:
            if algorithm == "LRU":
                recency.remove(page)
                recency.append(page)
        else:
            fault = True
            page_faults += 1
            if -1 in frames:
                idx = frames.index(-1)
            else:
                if algorithm == "LRU":
                    # Replace the least recently used page
                    lru_page = recency.popleft()
                    idx = frames.index(lru_page)
                elif algorithm == "Optimal":
                    # Replace the page that is used farthest in the future
                    future_uses = {}
                    for p in frames:
                        try:
                            future_uses[p] = page_refs[i+1:].index(p)
                        except ValueError:
                            future_uses[p] = float('inf')
                    idx = frames.index(max(future_uses, key=future_uses.get))
            frames[idx] = page
            if algorithm == "LRU":
                if page in recency:
                    recency.remove(page)
                recency.append(page)
        frame_history.append(frames.copy())
        fault_markers.append(fault)
    return page_faults, frame_history, fault_markers

def plot_frame_history_table(frame_history, page_refs, fault_markers):
    num_frames = len(frame_history[0])
    data = []
    for i, state in enumerate(frame_history):
        row = {"Reference": page_refs[i], "Fault": "Yes" if fault_markers[i] else ""}
        for j in range(num_frames):
            row[f"Frame {j+1}"] = state[j] if state[j] != -1 else ""
        data.append(row)
    df = pd.DataFrame(data)
    # Style: highlight fault rows in a soft red background.
    styled_df = df.style.apply(lambda x: ['background: #ffebee' if x.Fault=="Yes" else '' for _ in x], axis=1)\
                        .set_properties(**{'font-size': '14px', 'text-align': 'center'})
    st.dataframe(styled_df, height=300)

def plot_frame_history_heatmap(frame_history):
    # Create a matrix: rows represent page reference steps, columns are frame states.
    matrix = np.array(frame_history)
    # Replace -1 with np.nan for better visualization (shows as blank)
    matrix = np.where(matrix == -1, np.nan, matrix)
    
    # Setup a color palette
    num_colors = int(np.nanmax(matrix)) + 2 if np.nanmax(matrix)==np.nanmax(matrix) else 10
    cmap = sns.color_palette("Set2", num_colors)
    
    fig, ax = plt.subplots(figsize=(12, len(frame_history)*0.5+2))
    sns.heatmap(matrix, annot=True, fmt=".0f", cmap=cmap, cbar=False, linewidths=1,
                linecolor='gray', ax=ax, square=True, annot_kws={"size": 12}, mask=np.isnan(matrix))
    ax.set_xlabel("Frames", fontsize=12, fontweight='bold')
    ax.set_ylabel("Page Reference Step", fontsize=12, fontweight='bold')
    ax.set_title("Frame Status Over Time (Heatmap)", fontsize=14, fontweight='bold')
    st.pyplot(fig)

# ===========================
# Memory Fragmentation Simulation
# ===========================
def simulate_memory_fragmentation(total_memory, block_size, num_allocs, num_deallocs):
    memory = [None] * total_memory
    allocations = {}
    allocation_id = 1
    
    # Allocation phase: allocate contiguous blocks if available
    for _ in range(num_allocs):
        start = None
        for i in range(total_memory - block_size + 1):
            if all(memory[j] is None for j in range(i, i + block_size)):
                start = i
                break
        if start is None:
            break  # No contiguous free space available
        for j in range(start, start + block_size):
            memory[j] = allocation_id
        allocations[allocation_id] = (start, start + block_size - 1)
        allocation_id += 1

    # Deallocation phase: randomly free some allocations to simulate fragmentation
    deallocated = set(random.sample(list(allocations.keys()), min(num_deallocs, len(allocations))))
    for alloc in deallocated:
        start, end = allocations[alloc]
        for j in range(start, end + 1):
            memory[j] = None

    return memory, allocations, deallocated

def plot_memory_fragmentation(memory):
    fig, ax = plt.subplots(figsize=(12, 3))
    colors = {}
    color_list = plt.cm.Paired.colors  # Using a paired colormap for clear distinction
    color_idx = 0

    for i, block in enumerate(memory):
        if block is None:
            color = 'white'
            edgecolor = 'gray'
        else:
            if block not in colors:
                colors[block] = color_list[color_idx % len(color_list)]
                color_idx += 1
            color = colors[block]
            edgecolor = 'black'
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor=edgecolor, lw=1))
    
    ax.set_xlim(0, len(memory))
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, len(memory)+1, max(1, len(memory)//10)))
    ax.set_yticks([])
    ax.set_title("Memory Fragmentation Visualization", fontsize=14, fontweight='bold')
    ax.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.5)
    st.pyplot(fig)

# ===========================
# App Layout and UI
# ===========================
if sim_type == "Page Replacement Simulation":
    st.header("Page Replacement Simulation")
    
    # Sidebar inputs for page replacement simulation
    num_frames = st.sidebar.number_input("Number of Frames", min_value=1, max_value=10, value=3, step=1)
    sequence = st.sidebar.text_input("Page Reference Sequence (comma separated)", "1,2,3,2,4,1,5,2,1,2,3,4,5")
    algorithm = st.sidebar.selectbox("Replacement Algorithm", ["LRU", "Optimal"])
    
    try:
        page_refs = [int(x.strip()) for x in sequence.split(",")]
    except Exception as e:
        st.error("Invalid input for page reference sequence. Please enter integers separated by commas.")
        page_refs = []
    
    if st.button("Run Page Replacement Simulation"):
        if page_refs:
            faults, history, fault_markers = simulate_page_replacement(page_refs, num_frames, algorithm)
            st.success(f"Simulation complete! Total page faults: {faults}")
            st.subheader("Step-by-Step Frame History")
            plot_frame_history_table(history, page_refs, fault_markers)
            st.markdown("Rows highlighted in red indicate a page fault at that step.")
            st.subheader("Frame Status Heatmap")
            plot_frame_history_heatmap(history)
        else:
            st.warning("Please provide a valid page reference sequence.")

elif sim_type == "Memory Fragmentation Simulation":
    st.header("Memory Fragmentation Simulation")
    
    # Sidebar inputs for memory fragmentation simulation
    total_memory = st.sidebar.slider("Total Memory Size (units)", min_value=50, max_value=500, value=200, step=10)
    block_size = st.sidebar.slider("Block Size (units)", min_value=5, max_value=50, value=20, step=5)
    num_allocs = st.sidebar.slider("Number of Allocations", min_value=1, max_value=20, value=8, step=1)
    num_deallocs = st.sidebar.slider("Number of Deallocations", min_value=0, max_value=10, value=3, step=1)
    
    if st.button("Simulate Fragmentation"):
        memory, allocations, deallocated = simulate_memory_fragmentation(total_memory, block_size, num_allocs, num_deallocs)
        st.success("Memory fragmentation simulation complete!")
        st.subheader("Memory Layout")
        plot_memory_fragmentation(memory)
        st.markdown("**Legend:** Each colored block represents an allocation. White blocks indicate free memory.")

st.markdown("---")
st.markdown("This tool is for educational purposes. Adjust the parameters to explore how different virtual memory management strategies affect system behavior.")
