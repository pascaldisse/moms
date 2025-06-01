using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace hds.auth{

	public class AuthSocket{
		
		private TcpListener tcpListener;
    	private Thread listenThread;
		private bool mainThreadWorking;
				

    	public AuthSocket(){
			this.mainThreadWorking = true;
      		this.tcpListener = new TcpListener(IPAddress.Any, 11000);
			Output.WriteLine("Auth server set and ready at port 11000");
      		this.listenThread = new Thread(new ThreadStart(ListenForClients));
    	}
		
		public void startServer(){
			this.listenThread.Start();
		}
		
		public void stopServer(){
			this.mainThreadWorking = false;
			this.tcpListener.Stop();
		}
	
		private  void ListenForClients(){
  			this.tcpListener.Start();

  			while (mainThreadWorking){
    			// Create a new thread per connected client	
    			TcpClient client = this.tcpListener.AcceptTcpClient();
    			Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClientComm));
    			clientThread.Start(client);
  			}
		}	
		
		
		private void HandleClientComm(object client){
  			TcpClient tcpClient = (TcpClient)client;
  			NetworkStream clientStream = tcpClient.GetStream();
			bool working = true;
			
			// Define a auth server processor per thread
			AuthServer auth = new AuthServer(); 
			
  			byte[] message = new byte[2048];
  			int bytesRead;
			
			Output.WriteLine("[AUTH] Client Connected.");
  			
			// Send initial handshake packet
			// Based on the protocol, we need to send an initial packet with opcode that triggers AS_GetPublicKey_Request
			// The packet format appears to be [size, opcode, data...]
			// We'll send a simple "connection established" packet with opcode 0x01
			byte[] initPacket = new byte[] { 
				0x04, 0x00,  // Size (4 bytes total, little endian)
				0x01,        // Initial handshake opcode 
				0x00         // Empty data
			};
			
			try {
				Output.WriteLine("[AUTH] Sending initial handshake packet to client...");
				clientStream.Write(initPacket, 0, initPacket.Length);
				clientStream.Flush();
				Output.WriteLine("[AUTH] Initial packet sent, waiting for client response...");
			} catch (System.Exception ex) {
				Output.WriteLine("[AUTH] Failed to send initial packet: " + ex.Message);
			}
			
			// Receive TCP auth packets from the connected client.
			while (working){
    			bytesRead = 0;

	    		try{ 
					bytesRead = clientStream.Read(message, 0, 2048);
				}
				catch{ break; }
	
	    		if (bytesRead == 0)
	            	break;
				
				// Parse the received packet data
				try{
    				byte[] response = auth.processPacket(message,bytesRead);
				
					/* Check if auth says that it's done already */
					
					clientStream.Write(response,0,response.Length);
					
					if (auth.getStatus() ==-1){
						Output.WriteLine("[AUTH] World List sent, closing connection.");	
						break;
					}

				}catch(AuthException authE){
					Output.WriteLine(authE);
					break;
				}
				
  			}

  			Output.WriteLine("[AUTH] Client treatment thread ended");
  			tcpClient.Close();
			clientStream.Close();
		}	
	}	
}