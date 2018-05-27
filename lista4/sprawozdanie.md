Szymon Wróbel - Lista 4
===

Zadanie polega na takim wykorzystaniu potwierdzeń i numerów sekwencyjnych przez nadawcę i odbiorcę, aby odbiorca wydrukował wszystkie pakiety w kolejności ich numerów sekwencyjnych nawet jeśli połączenie w obie strony odbywa się przez Z2Frowarder. Nadawca może przypuszczać, że pakiet nie dotarł do celu jeśli przez długi czas nie otrzyma potwierdzenia od odbiorcy Może wtedy ten pakiet ponownie wysłać (retransmitować). Odbiorca może wykorzystywać numery sekwencyjne pakietów aby się zorientować czy ma prawo drukować dany pakiet, czy też musi czekać na brakujące wcześniejsza pakiety albo dany pakiet już był drukowany (np. jest duplikatem).

Opis plików
---
* `run.sh`
> Skrypt odpalający Z2Sender i Z2Receiver, oraz zapisujący odebrane dane do `rec.log`.

* `run_fwd.sh`
> Skrypt odpalający Z2Sender, dwie instance Z2Forwarder i Z2Receiver, oraz zapisujący odebrane dane do `rec_fwd.log`.
