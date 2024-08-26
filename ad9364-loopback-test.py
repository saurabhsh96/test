import iio
import numpy as np
import time

# Create IIO context
ctx = iio.Context()

# Find AD9364 device
try:
    ad9364_phy = ctx.find_device("ad9361-phy")
    ad9364_tx = ctx.find_device("cf-ad9361-dds-core-lpc")
    ad9364_rx = ctx.find_device("cf-ad9361-lpc")
except:
    print("AD9364 device not found!")
    exit(1)

# Configure AD9364
ad9364_phy.attrs["rx_lo_freq"].value = "2000000000"
ad9364_phy.attrs["tx_lo_freq"].value = "2000000000"
ad9364_phy.attrs["sampling_frequency"].value = "1000000"

# Enable channels
rx_chan = ad9364_rx.find_channel("voltage0")
tx_chan = ad9364_tx.find_channel("voltage0", True)
rx_chan.enabled = True
tx_chan.enabled = True

# Set buffer sizes
ad9364_rx.attrs["buffer_size"].value = "1024"
ad9364_tx.attrs["buffer_size"].value = "1024"

# Create data to transmit
data_0xAA = np.ones(1024, dtype=np.uint16) * 0xAA
data_0x55 = np.ones(1024, dtype=np.uint16) * 0x55

print("Starting loopback test...")

try:
    while True:
        # Transmit 0xAA
        tx_chan.write(data_0xAA.tobytes())
        time.sleep(0.1)  # Wait for transmission
        rx_data = np.frombuffer(rx_chan.read(1024), dtype=np.uint16)
        print("Sent 0xAA, Received:", hex(int(np.mean(rx_data))))

        # Transmit 0x55
        tx_chan.write(data_0x55.tobytes())
        time.sleep(0.1)  # Wait for transmission
        rx_data = np.frombuffer(rx_chan.read(1024), dtype=np.uint16)
        print("Sent 0x55, Received:", hex(int(np.mean(rx_data))))

except KeyboardInterrupt:
    print("Test stopped by user")

finally:
    # Cleanup
    del ctx
    print("Test completed")
