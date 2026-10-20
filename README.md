# 🛡️ OS Memory Leak Detector & Dynamic Heap Visualizer

An interactive Operating Systems project designed to monitor, track, and detect dynamic memory leaks in real time using a simulated virtual heap allocator and a web-based diagnostic dashboard.

Developed for **21CSC202J — Operating Systems** at **SRM Institute of Science and Technology**.

---

## 📌 Problem Statement
Dynamic memory management is a fundamental responsibility of operating systems. When user applications request memory on the **Heap** via system calls (such as `malloc()`) but fail to return it (via `free()`), the stranded memory causes a **Memory Leak**. 

Continuous memory leaks lead to:
1. **Memory Exhaustion** — Rapid consumption of physical RAM.
2. **System Thrashing** — Excessive paging/swapping to disk storage.
3. **Out-of-Memory (OOM) Crashes** — Kernel-level process termination.

---

## 🚀 Key Features

* **Live Virtual Heap Visualizer:** A dynamic RAM bar that renders memory chunks in real-time as they are allocated or freed.
* **Allocation Registry Table:** Tracks metadata for every block (Simulated Hex Address, Tag, Size in Bytes, and Timestamp).
* **Double-Free Detection:** Flags attempts to deallocate the same memory address more than once.
* **Automated Scenario Simulations:**
  * **Clean Execution:** Demonstrates a healthy program where all allocations are properly deallocated.
  * **Leaky Execution:** Demonstrates a buggy program that leaves stranded heap blocks.
* **Auditing Engine with Alarm Visuals:** Running a leak audit turns unfreed blocks into a **pulsing neon red alarm** state and displays an itemized diagnostic report.
* **Event Logging Console:** Terminal-style logging showing all allocation, free, and warning events.

---

## 🧠 Core Operating System Concepts Demonstrated

| OS Concept | Implementation in this Tool |
| :--- | :--- |
| **Heap Memory Pool** | Fixed simulated byte pool (`100,000 Bytes`) managed dynamically. |
| **`malloc()` Emulation** | Reserves contiguous byte chunks and assigns a virtual hexadecimal address (`0x70...`). |
| **`free()` Emulation** | Reclaims assigned memory and updates available RAM metrics. |
| **Allocation Metadata** | Stores block ID, virtual address, byte size, tag, and allocation timestamp. |
| **Double Free Protection** | Intercepts deallocation calls to addresses not found in the active table. |
| **Memory Leak Detection** | Audits the allocation registry at program termination for unreturned memory blocks. |

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Styling & Icons:** Bootstrap 5, Bootstrap Icons, Google Fonts (*Plus Jakarta Sans* & *JetBrains Mono*)
* **Cloud Platform:** Vercel Serverless Functions

---

## 💻 Local Setup & Execution

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/os-memory-leak-detector.git
   cd os-memory-leak-detector
