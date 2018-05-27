Szymon Wróbel - Lista 4
===

Zadanie polega na takim wykorzystaniu potwierdzeń i numerów sekwencyjnych przez nadawcę i odbiorcę, aby odbiorca wydrukował wszystkie pakiety w kolejności ich numerów sekwencyjnych nawet jeśli połączenie w obie strony odbywa się przez Z2Frowarder. Nadawca może przypuszczać, że pakiet nie dotarł do celu jeśli przez długi czas nie otrzyma potwierdzenia od odbiorcy Może wtedy ten pakiet ponownie wysłać (retransmitować). Odbiorca może wykorzystywać numery sekwencyjne pakietów aby się zorientować czy ma prawo drukować dany pakiet, czy też musi czekać na brakujące wcześniejsza pakiety albo dany pakiet już był drukowany (np. jest duplikatem).

Opis plików
---
* `Z2Sender.java`
> Klasa, której zadaniem jest wysyłanie danych oraz upewnienie się, że dane dotarły.

* `Z2Forwarder.java`
> Klasa symulująca połączenie, z możliwością duplikacji i utraty pakietu.

* `Z2Receiver.java`
> Klasa przyjmująca dane.

* `Z2Packet.java`
> Klasa opakowująca wysłane dane.

* `TimedPacket.java`
> Klasa dekorująca pakiet czasem retransmisji.

* `run.sh`
> Skrypt odpalający Z2Sender i Z2Receiver, oraz zapisujący odebrane dane do `rec.log`.

* `run_fwd.sh`
> Skrypt odpalający Z2Sender, dwie instance Z2Forwarder i Z2Receiver, oraz zapisujący odebrane dane do `rec_fwd.log`.

Modyfikacje klas
---

* `Z2Packet`

    Dodałem metody odczytujące numer sekwencyjny oraz ładunek (tutaj pojedynczy znak)

* `Z2Sender`
    
    Dodałem kolejkę przechowującą wysłane pakiety oraz słownik przechowujący potwierdzenia.

    Dodałem także wątek `RetransmitterThread` sprawdzający, czy otrzymaliśmy potwierdzenie, a w przeciwnym wypadku retransmitujący.

    Główną częścią tego wątku jest funkcja

    ```java
    private boolean checkIfConfirmed() throws Exception {
        TimedPacket tp = packetsSent.peek();
        Z2Packet sentPacket = tp.getPacket();
        Integer sentId = sentPacket.getId();
        char payload = sentPacket.getPayload();

        synchronized (confirmationsLock) {
            if (confirmations.contains(sentId)) {
                packetsSent.poll();
                System.out.println(
                    "Confirmed [" +
                    sentId + 
                    "]: " + 
                    payload
                );
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
    ```

    Sprawdza ona, czy otrzymaliśmy potwierdzenie najstarszego wysłanego pakietu, a jeśli nie, a upłynął czas do retransmisji, jest on ponownie wysyłany i dodawany na koniec kolejki pakietów.

* `Z2Forwarder`

    bez zmian

* `Z2Receiver`

    Dodałem licznik pamiętający następny oczekiwany pakiet, oraz słownik pamiętający otrzymane dane.

    Po otrzymaniu pakietu, wywoływana jest funkcja `checkReceived()`:
    ```java
    private boolean checkNext() {
        if (packets.containsKey(nextIdx)) {
            System.out.println("Received [" + nextIdx + "]: " + packets.get(nextIdx));
            ++nextIdx;
            return true;
        }
        return false;
    }

    public void checkReceived() {
        for (;;) {
            if (!checkNext()) break;
        }
    }
    ```

    jej działanie polega na sprawdzaniu czy mamy następny oczekiwany pakiet, a następnie wypisywaniu go (checkNext). Jest to powtarzane, dopóki udało nam się odnaleźć oczekiwany pakiet.

Przykładowe logi
---

#### Bez forwardera
* Z2Sender

    ```
    Sent [0]
    Confirmed [0]: A
    Sent [1]
    Confirmed [1]: l
    Sent [2]
    Confirmed [2]: a
    Sent [3]
    Confirmed [3]:
    Sent [4]
    Confirmed [4]: m
    Sent [5]
    Confirmed [5]: a
    Sent [6]
    Confirmed [6]:
    Sent [7]
    Confirmed [7]: k
    Sent [8]
    Confirmed [8]: o
    Sent [9]
    Confirmed [9]: t
    Sent [10]
    Confirmed [10]: a
    Sent [11]
    Confirmed [11]: .
    Sent [12]
    Confirmed [12]:
    ```

* Z2Receiver

    ```
    Received [0]: A
    Received [1]: l
    Received [2]: a
    Received [3]:  
    Received [4]: m
    Received [5]: a
    Received [6]:  
    Received [7]: k
    Received [8]: o
    Received [9]: t
    Received [10]: a
    Received [11]: .
    Received [12]: 
    ```

#### Z forwarderem

* Z2Sender

    ```
    Sent [0]
    Sent [1]
    Sent [2]
    Sent [3]
    Sent [4]
    Sent [5]
    Retransmit 0
    Sent [0]
    Retransmit 1
    Sent [1]
    Sent [6]
    Sent [7]
    Retransmit 2
    Sent [2]
    Sent [8]
    Retransmit 3
    Sent [3]
    Sent [9]
    Retransmit 4
    Sent [4]
    Sent [10]
    Retransmit 0
    Sent [0]
    Sent [11]
    (...)
    Sent [30]
    Sent [36]
    Retransmit 20
    Sent [37]
    Sent [20]
    Confirmed [10]: a
    Confirmed [15]: a
    Retransmit 5
    Sent [5]
    Confirmed [6]:
    Confirmed [11]: .
    Retransmit 16
    Sent [16]
    Retransmit 21
    Sent [21]
    Retransmit 26
    Sent [26]
    Retransmit 31
    Sent [31]
    Retransmit 7
    Sent [7]
    ```

* Z2Receiver

    ```
    Received [0]: A
    Received [1]: l
    Received [2]: a
    Received [3]:  
    Received [4]: m
    Received [5]: a
    Received [6]:  
    Received [7]: k
    Received [8]: o
    Received [9]: t
    Received [10]: a
    Received [11]: .
    Received [12]: 

    Received [13]: O
    Received [14]: l
    Received [15]: a
    Received [16]:  
    Received [17]: n
    Received [18]: i
    Received [19]: e
    ```