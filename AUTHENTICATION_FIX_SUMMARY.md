# Matrix Online Authentication Server Fix

## Problem Identified
The Matrix Online client and server are stuck in a deadlock situation:
- **Client**: Waiting for the server to send data first after connecting
- **Server**: Waiting for the client to send the first packet (AS_GetPublicKeyRequest)

This prevents any authentication from happening as both sides are waiting for the other.

## Root Cause
In `AuthSocket.cs`, the server immediately calls `clientStream.Read()` after accepting a connection, blocking until the client sends data. However, the client is also waiting for an initial packet from the server before it will send anything.

## Solution
Modify the server to send an initial packet immediately after accepting a client connection. This will trigger the client to start the authentication handshake by sending the AS_GetPublicKeyRequest packet.

## Implementation
Three different fix versions have been created:

### Version 1: Simple Empty Packet (`AuthSocket_Fixed.cs`)
- Sends a minimal `0x00 0x00` packet
- Simplest approach to break the deadlock

### Version 2: Handshake Packet (`AuthSocket_FixedV2.cs`)
- Sends a structured packet with opcode `0x01`
- Format: `[0x04, 0x00, 0x01, 0x00]` (size + opcode + data)

### Version 3: Server Ready Packet (`AuthSocket_FixedV3.cs`)
- Sends opcode `0x05` which might be the expected "server ready" signal
- Format: `[0x02, 0x05]` (size + opcode)
- Includes additional debug logging

## How to Apply the Fix

### Manual Method:
```bash
# Backup the original file
sudo cp /Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020/hds/auth/AuthSocket.cs \
        /Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020/hds/auth/AuthSocket.cs.backup

# Apply one of the fixes (example with version 3)
sudo cp /Users/pascaldisse/Downloads/mxo/AuthSocket_FixedV3.cs \
        /Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020/hds/auth/AuthSocket.cs
```

### Using the Script:
```bash
cd /Users/pascaldisse/Downloads/mxo
./apply_auth_fix.sh
# Follow the prompts to choose which version to apply
```

## After Applying the Fix

1. **Rebuild the server:**
   ```bash
   cd /Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020
   msbuild /p:Configuration=Debug /p:Platform=x86
   ```

2. **Restart the server:**
   ```bash
   cd /Users/pascaldisse/Downloads/mxo/mxo-hd-nov2020/hds/bin/Debug
   mono hds.exe
   ```

3. **Test with the client:**
   - Start the Matrix Online client
   - Attempt to connect to localhost
   - Check the server logs for the new debug messages

## Expected Behavior After Fix
1. Client connects to port 11000
2. Server sends initial packet
3. Client responds with AS_GetPublicKeyRequest (opcode 0x06)
4. Normal authentication flow continues

## Debug Output
With the fixed versions, you should see:
```
[AUTH] Client Connected.
[AUTH] Sending initial packet to client...
[AUTH] Initial packet sent, waiting for client response...
[AUTH] Received X bytes from client
[AUTH] First 3 bytes: XX XX XX
```

## Troubleshooting
- If the client still doesn't respond, try a different fix version
- Check that the server is actually using the modified code (rebuild required)
- Monitor network traffic with Wireshark to see what's actually being sent
- The client might expect a specific packet format - version 3 includes debug logging to help identify this

## Technical Details
- **Port**: TCP 11000 (Auth Server)
- **Expected Flow**: 
  1. Server → Client: Initial packet
  2. Client → Server: AS_GetPublicKeyRequest (0x06)
  3. Server → Client: AS_GetPublicKeyReply (0x07)
  4. Client → Server: AS_HandleAuth_Request (0x08)
  5. Server → Client: AS_HandleAuth_Reply (0x09)
  6. Client → Server: AS_HandleAuthChallenge_Response (0x0A)
  7. Server → Client: World list and character data