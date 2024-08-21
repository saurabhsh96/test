import iio
import numpy as np

# Connect to the FMCOMM4 device locally
ctx = iio.Context()

# Get the transmit and receive devices
tx = ctx.find_device("cf-ad9361-dds-core-lpc")
rx = ctx.find_device("cf-ad9361-lpc")

# Configure the transmit channels
tx_chan0 = tx.find_channel("voltage0")
tx_chan1 = tx.find_channel("voltage1")

# Configure the receive channels
rx_chan0 = rx.find_channel("voltage0")
rx_chan1 = rx.find_channel("voltage1")

# Enable the channels
tx_chan0.enabled = True
tx_chan1.enabled = True
rx_chan0.enabled = True
rx_chan1.enabled = True

# Set the sample rate (must be the same for TX and RX)
sample_rate = 1e6  # 1 MHz
tx_chan0.samplerate = sample_rate
rx_chan0.samplerate = sample_rate

# Set the center frequency (must be the same for TX and RX)
center_freq = 915e6  # 915 MHz
tx_chan0.frequency = center_freq
rx_chan0.frequency = center_freq

# Generate a simple sine wave signal
duration = 1  # seconds
t = np.linspace(0, duration, int(duration * sample_rate), False)
signal = np.sin(2 * np.pi * 100e3 * t)  # 100 kHz sine wave

# Normalize the signal
signal = signal * 2**15  # Scale to 16-bit range

# Prepare the signal for transmission (I/Q format)
iq_signal = np.empty((signal.size * 2,), dtype=np.int16)
iq_signal[0::2] = signal.astype(np.int16)  # I (in-phase)
iq_signal[1::2] = signal.astype(np.int16)  # Q (quadrature)

# Transmit the signal
tx_chan0.push(iq_signal)
print("Signal transmitted successfully.")

# Prepare for reception
buffer_size = len(iq_signal)
rx_buffer = iio.Buffer(rx, buffer_size)

# Receive the signal
rx_buffer.refill()
data = rx_buffer.read()

# Convert the received data to a numpy array
rx_signal = np.frombuffer(data, dtype=np.int16)

# Separate I and Q components
i_data = rx_signal[0::2]
q_data = rx_signal[1::2]

# Print some statistics about the received signal
print("Received signal statistics:")
print(f"I channel - Mean: {np.mean(i_data):.2f}, Max: {np.max(i_data)}, Min: {np.min(i_data)}")
print(f"Q channel - Mean: {np.mean(q_data):.2f}, Max: {np.max(q_data)}, Min: {np.min(q_data)}")

# Save the received data to a file
np.savez('received_signal.npz', i_data=i_data, q_data=q_data)
print("Received signal data saved to 'received_signal.npz'")
