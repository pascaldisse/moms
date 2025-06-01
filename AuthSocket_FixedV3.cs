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
  			
			// Alternative approach: Try to trigger the client by sending a minimal packet
			// that might be what the client is waiting for
			// Based on the packet structure in AuthServer, let's try sending just the opcode
			// for "server ready" or similar
			byte[] initPacket = new byte[] { 
				0x02,  // Size byte (indicating 2 bytes total)
				0x05   // A different opcode that might trigger the client to send AS_GetPublicKey_Request (0x06)
			};
			
			try {
				Output.WriteLine("[AUTH] Sending server ready packet to client...");
				clientStream.Write(initPacket, 0, initPacket.Length);
				clientStream.Flush();
				Output.WriteLine("[AUTH] Server ready packet sent, waiting for AS_GetPublicKey_Request...");
			} catch (System.Exception ex) {
				Output.WriteLine("[AUTH] Failed to send initial packet: " + ex.Message);
			}
			
			// Receive TCP auth packets from the connected client.
			while (working){
    			bytesRead = 0;

	    		try{ 
					bytesRead = clientStream.Read(message, 0, 2048);
					if (bytesRead > 0) {
						Output.WriteLine("[AUTH] Received " + bytesRead + " bytes from client");
						// Log first few bytes for debugging
						if (bytesRead >= 3) {
							Output.WriteLine("[AUTH] First 3 bytes: " + 
								message[0].ToString("X2") + " " + 
								message[1].ToString("X2") + " " + 
								message[2].ToString("X2"));
						}
					}
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