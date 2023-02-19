// Server side 
// to compile: javac -d . Server.java
// to run:     java socket_demo.Server

package socket_demo;

import java.net.*;
import java.io.*;

public class Server {

    private Socket socket = null;
    private ServerSocket server = null;
    private DataInputStream in  = null;

    public Server(int port) {
        try {
            server = new ServerSocket(port);
            System.out.println(String.format("Server Started on port %s", port));
            System.out.println("Waiting for a client ...");

            socket = server.accept();
            System.out.println("Client accepted");

            in = new DataInputStream(
                new BufferedInputStream(socket.getInputStream()));

            String line = "";

            while (!line.equals("Over")) {
                try {
                    line = in.readUTF();
                    System.out.println(line);
                } catch (IOException ex) {
                    System.out.println(ex);
                }

            }
            System.out.println("Closing Connection");
            socket.close();
            in.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
    }

    public static void main(String[] args) 
    {
        Server server = new Server(5000);
    }
}