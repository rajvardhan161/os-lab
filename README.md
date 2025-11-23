🚀 Virtual Memory Simulator

A powerful and interactive Streamlit-based Virtual Memory Simulator that helps students understand how operating systems manage memory using Page Replacement Algorithms and Memory Fragmentation Techniques.

This project is part of Operating Systems learning and provides clear visualization of LRU, Optimal Algorithm, and Dynamic Memory Fragmentation.

⸻

✨ Features

🔹 1. Page Replacement Simulation

Simulate how operating systems allocate memory using:
	•	LRU (Least Recently Used)
	•	Optimal Page Replacement Algorithm

Visual Outputs:
	•	📋 Step-by-step frame table
	•	🔥 Highlighted page faults
	•	🎨 Beautiful heatmap visualization of frame changes over time

⸻

🔹 2. Memory Fragmentation Simulation

Visualize dynamic memory allocation and fragmentation:
	•	Random allocation & deallocation
	•	Colored blocks representing allocated memory
	•	White blocks representing fragmented/free spaces
	•	Clean horizontal memory map visualization

⸻

🛠️ Tech Stack
	•	Python
	•	Streamlit
	•	NumPy
	•	Pandas
	•	Matplotlib
	•	Seaborn
	•	Deque (Collections)

⸻

📂 Project Structure
Virtual-Memory-Simulator/
│
├── virtual_memory_simulator.py   # Main Streamlit App
├── requirements.txt              # Required Python libraries
└── README.md                     # Documentation

📌 How to Run the Project

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/Virtual-Memory-Simulator.git
cd Virtual-Memory-Simulator
2. Install Dependencies
pip install -r requirements.txt
3. Run the Streamlit App
streamlit run virtual_memory_simulator.py

📸 Screenshots (Optional)

You can add:
	•	Page table visualization
	•	Heatmap output
	•	Fragmentation chart

⸻

🔧 How It Works

Page Replacement Module
	•	Reads input page reference string
	•	Applies selected algorithm (LRU/Optimal)
	•	Tracks:
	•	Frame updates
	•	Page faults
	•	History of allocations

Memory Fragmentation Module
	•	Creates a 1D memory map
	•	Allocates blocks
	•	Randomly deallocates to simulate fragmentation
	•	Renders the memory blocks visually

⸻

🎯 Learning Outcomes

Students using this tool can:
	•	Understand how virtual memory works
	•	Visualize page faults
	•	Compare different page replacement strategies
	•	Learn dynamic allocation & fragmentation behavior
	•	Enhance OS conceptual clarity

⸻

🧑‍💻 Author

Rajvardhan
B.Tech CSE | Lovely Professional University
Passionate about system-level concepts, OS, and full-stack development.

⸻

📜 License

This project is open-source under the MIT License.

⸻

⭐ Contribution

Contributions are welcome!
Feel free to:
	•	Submit issues
	•	Create pull requests
	•	Suggest improvements
