package socket_demo;

import java.io.*;
import java.net.*;

public class Client {
    private Socket socket = null;
    private BufferedReader input = null;
    private DataOutputStream out = null;

    public Client(String address, int port)
    {
        try {
            socket = new Socket(address, port);
            System.out.println("Connected");

            input = new BufferedReader(new InputStreamReader(System.in));

            out = new DataOutputStream(socket.getOutputStream());
        } catch (IOException ex) {
            System.out.println(ex);
            return;
        }

        String line = "";

        while (!line.equals("Over")) {
            try {
                line = input.readLine();
                out.writeUTF(line);
            } catch (IOException ex) {
                System.out.println(ex);
            }
        }

        try {
            input.close();
            out.close();
            socket.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
    }

    public static void main(String args[]) {
        Client client = new Client("127.0.0.1", 5000);
    }
}
