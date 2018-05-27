Lista 4
===

Zadanie 1
---

Przykładowe programy: Z2Forwarder.java, Z2Packet.java, Z2Receiver.java, Z2Sender.java. Plik plik.txt zawiera przykładowe dane.

Program Z2Sender wysyła w osobnych datagramach po jednym znaku wczytanym z wejścia do portu o numerze podanym jako drugi parametr wywołania programu. Jednocześnie drukuje na wyjściu informacje o pakietach otrzymanych w porcie podanym jako pierwszy parametr wywołania. 

Program Z2Receiver drukuje informacje o każdym pakiecie, który otrzymał w porcie o numrze podanym jako pierwszy parametr wywołania programu i odsyła go do portu podanego jako drugi paramer wywołania programu. 

Klasa Z2Packet, umożliwia wygodne wstawianie i odczytywanie czterobajtowych liczb całkowitych do tablicy bajtów przesyłanych w datagramie - metody: public void setIntAt(int value, int idx) oraz public int getIntAt(int idx). Wykorzystane jest to do wstawiania i odczytywania numerów sekwencyjnych pakietów.

Po skompilowaniu, można je uruchomić w terminalu w następujący sposób: 
```bash
java Z2Receiver 6001 6000 &
java Z2Sender 6000 6001 < plik.txt
```

W tej konfiguracji Z2Receiver powinien otrzymywać wszystkie pakiety w odpowiedniej kolejności i bez strat, i odsyłane prze niego potwierdzenia, dochodzą do Z2Sender w taki sam (niezadwodny) sposób. 

Program Z2Sender po zakończeniu transmisji musi być ręcznie przerwany (CTRL+C), bo wątek odbierający oczekuje na kolejne pakiety. 

Program Z2Receiver można zatrzymać przy użyciu poleceń ps (aby odczytać nr procesu) i kill (aby wysłać do procesu sygnał zakończenia). 

W Internecie każdy pakiet przesyłany jest niezależnie i w miarę dostępnych możliwości. W związku z tym pakiety wysyłane przez nadawcę mogą być tracone, przybywać z różnymi opóźnieniami, w zmienionej kolejności, a nawet mogą być duplikowane. 

Program Z2Forwarder symuluje tego typu połączenie. Aby go użyć można wykonać (po zabiciu innych programów korzystających z portów 6000, 6001, 6002, 6003) następujące polecenia: 
```bash
java Z2Receiver 6002 6003 &
java Z2Forwarder 6001 6002 & 
java Z2Forwarder 6003 6000 & 
java Z2Sender 6000 6001 < plik.txt 
```

W tej konfiguracji pierwszy Z2Forwarder przekazuje pakiety od Z2Sender do Z2Receiver, a drugi - w przeciwnym kierunku. (Może wystąpić pewne opóźnienie, zanim zaczną się pojawiać wyniki drukowane przez Z2Receiver i Z2Sender.)

Zadanie polega na takim wykorzystaniu potwierdzeń i numerów sekwencyjnych przez nadawcę i odbiorcę, aby odbiorca wydrukował wszystkie pakiety w kolejności ich numerów sekwencyjnych nawet jeśli połączenie w obie strony odbywa się przez Z2Frowarder. 

Nadawca może przypuszczać, że pakiet nie dotarł do celu jeśli przez długi czas nie otrzyma potwierdzenia od odbiorcy Może wtedy ten pakiet ponownie wysłać (retransmitować). 

Odbiorca może wykorzystywać numery sekwencyjne pakietów aby się zorientować czy ma prawo drukować dany pakiet, czy też musi czekać na brakujące wcześniejsza pakiety albo dany pakiet już był drukowany (np. jest duplikatem).