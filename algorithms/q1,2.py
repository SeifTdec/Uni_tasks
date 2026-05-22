import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def generate_distributions(n=1000, seed=42):
    rng = np.random.default_rng(seed)

    data = {
        "Uniform": rng.uniform(0, 1, n),
        "Normal": rng.normal(0, 1, n),
        "Exponential": rng.exponential(scale=1.0, size=n),   # mean = 1/rate
        "Poisson": rng.poisson(lam=5, size=n),
        "Binomial": rng.binomial(n=10, p=0.5, size=n),
    }
    return data

def plot_distributions(data):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    # Uniform
    axes[0].hist(data["Uniform"], bins=30, edgecolor='black')
    axes[0].set_title("Uniform Distribution")
    axes[0].set_xlabel("Value")
    axes[0].set_ylabel("Frequency")

    # Normal
    axes[1].hist(data["Normal"], bins=30, edgecolor='black')
    axes[1].set_title("Normal Distribution")
    axes[1].set_xlabel("Value")
    axes[1].set_ylabel("Frequency")

    # Exponential
    axes[2].hist(data["Exponential"], bins=30, edgecolor='black')
    axes[2].set_title("Exponential Distribution")
    axes[2].set_xlabel("Value")
    axes[2].set_ylabel("Frequency")

    # Poisson
    axes[3].hist(data["Poisson"], bins=range(int(data["Poisson"].min()), int(data["Poisson"].max()) + 2),
                 edgecolor='black', align='left')
    axes[3].set_title("Poisson Distribution")
    axes[3].set_xlabel("Value")
    axes[3].set_ylabel("Frequency")

    # Binomial
    axes[4].hist(data["Binomial"], bins=range(int(data["Binomial"].min()), int(data["Binomial"].max()) + 2),
                 edgecolor='black', align='left')
    axes[4].set_title("Binomial Distribution")
    axes[4].set_xlabel("Value")
    axes[4].set_ylabel("Frequency")

    # Empty plot
    axes[5].axis("off")

    plt.tight_layout()
    plt.show()

# Generate and plot
dist_data = generate_distributions(n=1000, seed=42)
plot_distributions(dist_data)


from collections import deque

def simulate_mm1(lam=0.8, mu=1.2, sim_time=1000, seed=42):
    """
    M/M/1 simulation using exponential interarrival and service times.
    lam = arrival rate
    mu  = service rate
    sim_time = total simulation time
    """
    rng = np.random.default_rng(seed)

    current_time = 0.0
    next_arrival = rng.exponential(1 / lam)
    next_departure = float('inf')

    queue = deque()
    server_busy = False

    # Statistics
    total_busy_time = 0.0
    last_event_time = 0.0
    area_under_q = 0.0
    waiting_times = []

    # For plotting
    event_times = [0.0]
    queue_lengths = [0]
    server_states = [0]  # 0 = idle, 1 = busy

    while current_time < sim_time:
        # Choose next event
        if next_arrival < next_departure:
            current_time = next_arrival

            # Update time-average queue length
            area_under_q += queue_lengths[-1] * (current_time - last_event_time)
            last_event_time = current_time

            # Arrival
            if server_busy:
                queue.append(current_time)
            else:
                server_busy = True
                service_time = rng.exponential(1 / mu)
                next_departure = current_time + service_time
                waiting_times.append(0.0)

            # Schedule next arrival
            next_arrival = current_time + rng.exponential(1 / lam)

        else:
            current_time = next_departure

            # Update time-average queue length
            area_under_q += queue_lengths[-1] * (current_time - last_event_time)
            last_event_time = current_time

            # Departure
            if queue:
                arrival_time = queue.popleft()
                wait = current_time - arrival_time
                waiting_times.append(wait)

                service_time = rng.exponential(1 / mu)
                next_departure = current_time + service_time
            else:
                server_busy = False
                next_departure = float('inf')

        # Busy time tracking
        if server_busy:
            total_busy_time += current_time - event_times[-1]

        # Save state for plotting
        current_q_len = len(queue)
        event_times.append(current_time)
        queue_lengths.append(current_q_len)
        server_states.append(1 if server_busy else 0)

    avg_queue_length = area_under_q / sim_time
    utilization = total_busy_time / sim_time
    avg_waiting_time = np.mean(waiting_times) if waiting_times else 0.0

    results = {
        "avg_queue_length": avg_queue_length,
        "utilization": utilization,
        "avg_waiting_time": avg_waiting_time,
        "event_times": event_times,
        "queue_lengths": queue_lengths,
        "server_states": server_states,
        "waiting_times": waiting_times
    }
    return results

def plot_mm1(results):
    event_times = results["event_times"]
    queue_lengths = results["queue_lengths"]
    server_states = results["server_states"]
    waiting_times = results["waiting_times"]

    fig, axes = plt.subplots(3, 1, figsize=(14, 12))

    # Queue length over time
    axes[0].step(event_times, queue_lengths, where='post')
    axes[0].set_title("Queue Length Over Time")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Number waiting")

    # Server busy/idle over time
    axes[1].step(event_times, server_states, where='post')
    axes[1].set_title("Server State Over Time")
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("Busy = 1, Idle = 0")

    # Waiting time distribution
    axes[2].hist(waiting_times, bins=30, edgecolor='black')
    axes[2].set_title("Distribution of Waiting Times")
    axes[2].set_xlabel("Waiting Time")
    axes[2].set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()

# Run simulation
results = simulate_mm1(lam=0.8, mu=1.2, sim_time=1000, seed=42)

print("M/M/1 Simulation Results")
print("------------------------")
print(f"Average Queue Length: {results['avg_queue_length']:.4f}")
print(f"Utilization:          {results['utilization']:.4f}")
print(f"Average Waiting Time:  {results['avg_waiting_time']:.4f}")

plot_mm1(results)
