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

# Helper function to set attribute safely
def set_attr_safely(dev, attr, value):
    try:
        dev.attrs[attr].value = str(value)
    except KeyError:
        print(f"Warning: Attribute '{attr}' not found. Skipping.")
    except Exception as e:
        print(f"Error setting {attr}: {str(e)}")

# Configure AD9364
set_attr_safely(ad9364_phy, "rx_lo_freq", 2000000000)
set_attr_safely(ad9364_phy, "tx_lo_freq", 2000000000)
set_attr_safely(ad9364_phy, "trx_rate_governor", "nominal")
set_attr_safely(ad9364_phy, "sampling_frequency", 1000000)
set_attr_safely(ad9364_phy, "rx_rf_bandwidth", 1000000)
set_attr_safely(ad9364_phy, "tx_rf_bandwidth", 1000000)

# Enable channels
rx_chan = ad9364_rx.find_channel("voltage0")
tx_chan = ad9364_tx.find_channel("voltage0", True)
rx_chan.enabled = True
tx_chan.enabled = True

# Set buffer sizes
set_attr_safely(ad9364_rx, "buffer_size", 1024)
set_attr_safely(ad9364_tx, "buffer_size", 1024)

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
except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Cleanup
    del ctx
    print("Test completed")
