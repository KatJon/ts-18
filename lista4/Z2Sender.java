import java.net.*;
import java.util.*;

class Z2Sender {
    private static final int datagramSize = 50;
    private static final int sleepTime = 500;
    private static final int waitTime = 5;
    private InetAddress localHost;
    private int destinationPort;
    private DatagramSocket socket;
    private SenderThread sender;
    private ReceiverThread receiver;
    private RetransmitterTread retransmitter;

    private final Object packetsSentLock = new Object();
    private Queue<TimedPacket> packetsSent = new LinkedList<>();
    private final Object confirmationsLock = new Object();
    private HashSet<Integer> confirmations = new HashSet<>();

    private volatile int time;

    public Z2Sender(int myPort, int destPort) throws Exception {
        localHost = InetAddress.getByName("127.0.0.1");
        destinationPort = destPort;
        socket = new DatagramSocket(myPort);
        sender = new SenderThread();
        receiver = new ReceiverThread();
        retransmitter = new RetransmitterTread();
        time = 0;
    }

    private void sendPacket(Z2Packet p) throws Exception {
        DatagramPacket packet = new DatagramPacket(
                p.data, p.data.length, localHost, destinationPort
        );
        socket.send(packet);
        System.out.println("Sent [" + p.getIntAt(0) + "]");
    }

    private Z2Packet makePacket(int idx, byte x) throws Exception {
        Z2Packet p = new Z2Packet(4 + 1);
        p.setIntAt(idx, 0);
        p.data[4] = x;
        return p;
    }

    private TimedPacket makeTimed(Z2Packet p) {
        return new TimedPacket(time + waitTime, p);
    }

    class SenderThread extends Thread {
        public void run() {
            int i, x;
            try {
                for (i = 0; (x = System.in.read()) >= 0; i++) {
                    Z2Packet p = makePacket(i, (byte) x);
                    sendPacket(p);
                    synchronized (packetsSentLock) {
                        packetsSent.add(makeTimed(p));
                    }
                    sleep(sleepTime);
                    time++;
                }
            } catch (Exception e) {
                System.out.println("Z2Sender.SenderThread.run: " + e);
            }
        }
    }

    class ReceiverThread extends Thread {
        public void run() {
            try {
                while (true) {
                    byte[] data = new byte[datagramSize];
                    DatagramPacket packet = new DatagramPacket(data, datagramSize);
                    socket.receive(packet);

                    Z2Packet p = new Z2Packet(packet.getData());
                    Integer id = p.getIntAt(0);
                    synchronized (confirmationsLock) {
                        confirmations.add(id);
                    }
                }
            } catch (Exception e) {
                System.out.println("Z2Sender.ReceiverThread.run: " + e);
            }
        }
    }

    class RetransmitterTread extends Thread {
        private boolean checkIfConfirmed() throws Exception{
            TimedPacket tp = packetsSent.peek();
            Z2Packet sentPacket = tp.getPacket();
            Integer sentId = sentPacket.getId();
            char payload = sentPacket.getPayload();

            synchronized (confirmationsLock) {
                if (confirmations.contains(sentId)) {
                    packetsSent.poll();
                    System.out.println("Confirmed [" + sentId + "]: " + payload);
                } else if (tp.shouldRetransmit(time)) {
                    packetsSent.poll();
                    System.out.println("Retransmit " + sentId);
                    sendPacket(sentPacket);
                    packetsSent.add(makeTimed(sentPacket));
                } else {
                    return false;
                }
            }

            return true;
        }

        private boolean syncCheck() throws Exception {
            synchronized (packetsSentLock) {
                return checkIfConfirmed();
            }
        }

        public void run() {
            try {
                for (;;) {
                    if (packetsSent.isEmpty() || !syncCheck()) {
                        sleep(sleepTime);
                    }
                }
            } catch (Exception e) {
                System.out.println("Z2Sender.RetransmitterThread.run: " + e);
            }
        }
    }

    public static void main(String[] args)
            throws Exception {
        Z2Sender sender = new Z2Sender(
                Integer.parseInt(args[0]),
                Integer.parseInt(args[1])
        );
        sender.sender.start();
        sender.receiver.start();
        sender.retransmitter.start();
    }
}
