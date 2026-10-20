import datetime
import os
import random
from flask import Flask, jsonify, render_template, request

# Locate the 'templates' folder in the root directory
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, "templates")

app = Flask(__name__, template_folder=template_dir)


class MemoryBlock:
    """Represents an allocated block in heap memory with tracking metadata."""

    def __init__(self, block_id, address, size, tag):
        self.block_id = block_id
        self.address = address
        self.size = size
        self.tag = tag
        self.timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "id": self.block_id,
            "address": self.address,
            "size": self.size,
            "tag": self.tag,
            "timestamp": self.timestamp,
        }


class MemoryManager:
    """Simulates an OS Memory Management Subsystem."""

    def __init__(self, total_memory=100000):  # 100 KB total pool
        self.total_memory = total_memory
        self.used_memory = 0
        self.counter = 0
        self.table = {}  # Active allocation registry
        self.logs = []  # System event logs

    def log(self, message, msg_type="info"):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.logs.insert(
            0, {"time": time_str, "text": message, "type": msg_type}
        )
        if len(self.logs) > 30:
            self.logs.pop()

    def allocate(self, size, tag="Variable"):
        if self.used_memory + size > self.total_memory:
            self.log(
                f"Out of Memory! Cannot allocate {size} bytes for '{tag}'.",
                "danger",
            )
            return None

        self.counter += 1
        addr = hex(0x700000 + random.randint(1000, 99999))
        block = MemoryBlock(self.counter, addr, size, tag)
        self.table[addr] = block
        self.used_memory += size
        self.log(
            f"Allocated {size} bytes at {addr} for '{tag}'",
            "success",
        )
        return addr

    def deallocate(self, addr):
        if addr not in self.table:
            self.log(
                f"Double Free / Invalid Free attempt at {addr}!",
                "warning",
            )
            return False

        block = self.table.pop(addr)
        self.used_memory -= block.size
        self.log(
            f"Freed {block.size} bytes from {addr} ('{block.tag}')", "info"
        )
        return True

    def reset(self):
        self.used_memory = 0
        self.counter = 0
        self.table.clear()
        self.logs.clear()
        self.log("Memory pool reset.", "info")


# Global allocator instance
manager = MemoryManager()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(
        {
            "total_memory": manager.total_memory,
            "used_memory": manager.used_memory,
            "free_memory": manager.total_memory - manager.used_memory,
            "blocks": [b.to_dict() for b in manager.table.values()],
            "logs": manager.logs,
        }
    )


@app.route("/api/allocate", methods=["POST"])
def api_allocate():
    data = request.get_json(force=True) or {}
    size = int(data.get("size", 1024))
    tag = data.get("tag", "GeneralData")
    addr = manager.allocate(size, tag)
    return jsonify({"success": addr is not None, "address": addr})


@app.route("/api/deallocate", methods=["POST"])
def api_deallocate():
    data = request.get_json(force=True) or {}
    addr = data.get("address")
    success = manager.deallocate(addr)
    return jsonify({"success": success})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    manager.reset()
    return jsonify({"success": True})


@app.route("/api/simulate/leaky", methods=["POST"])
def simulate_leak():
    manager.reset()
    ptr1 = manager.allocate(15000, "Image_Texture")
    ptr2 = manager.allocate(25000, "Audio_Buffer")
    ptr3 = manager.allocate(18000, "User_Session_Leak")
    ptr4 = manager.allocate(12000, "Network_Packets_Leak")

    # Frees only ptr1 and ptr2; ptr3 and ptr4 are leaked!
    manager.deallocate(ptr1)
    manager.deallocate(ptr2)
    manager.log(
        "SIMULATION: Program exited leaving 2 active blocks in RAM!", "warning"
    )
    return jsonify({"success": True})


@app.route("/api/simulate/clean", methods=["POST"])
def simulate_clean():
    manager.reset()
    ptr1 = manager.allocate(20000, "Render_Buffer")
    ptr2 = manager.allocate(10000, "Temp_Cache")
    manager.deallocate(ptr1)
    manager.deallocate(ptr2)
    manager.log(
        "SIMULATION: All memory allocated was properly deallocated.", "success"
    )
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
