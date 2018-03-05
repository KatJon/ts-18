# Technologie sieciowe - Lista 1
## Zadanie 1
Przetestuj działanie programów:
### `ping`
> Komendy wykorzystane przeze mnie różnią się od standardowych, ze względu na system operacyjny (macOS), w którym występuje `ping` w wersji z rodziny BSD
>+ `-m ttl` TTL
>+ `-D` flaga "Nie fragmentuj"
>+ `-s n` rozmiar pakietu 

#### Badane serwery
* `chinadaily.com.cn` (Pekin)
* `onet.pl` (Kraków)   

#### Znajdowanie odległości *do*
Szukamy najmniejszego TTL, dla którego żądanie ping dotrze
```console
λ: ~$ ping -s 32 -m 29 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 32 data bytes
Request timeout for icmp_seq 0
```

```console
λ: ~$ ping -s 32 -m 30 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 32 data bytes
40 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=576.853 ms
```

* Odległość: `30 przeskoków`

#### Znajdowanie odległości *z powrotem*
```console
λ: ~$ ping -s 32 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 32 data bytes
40 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=427.869 ms
```

* TTL otrzymane: `35`
* Odległość:
Wyznaczenie odległości z powrotem jest problematyczne, ze względu na nieznaną początkową wartość TTL ustawioną przez serwer. Możliwe wyniki
    + `64 - 35 = 29 przeskoków` 
    + `128 - 35 = 93 przeskoki`

Najprawdopobniejsza wydaje się odpowiedź `29`, która jest zbliżona do drogi *do*

#### Największy możliwy niefragmentowany pakiet
```console
λ: ~$ ping -D -s 996 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 996 data bytes
1004 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=507.230 ms
```

```console
λ: ~$ ping -D -s 997 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 997 data bytes
Request timeout for icmp_seq 0
```

Wyniki uzyskane dla chińskiego hosta mogą wynikać z architektury chińskiej sieci.

Dla porównania `onet.pl`:

```console
λ: ~$ ping -D -s 1472 onet.pl
PING onet.pl (213.180.141.140): 1472 data bytes
1480 bytes from 213.180.141.140: icmp_seq=0 ttl=59 time=14.323 ms
```

```console
λ: ~$ ping -D -s 1473 onet.pl
PING onet.pl (213.180.141.140): 1473 data bytes
ping: sendto: Message too long
```

A więc maksymalna wielkość niefragmentowanego pakietu wynosi dla chińskiego hosta `996`, a dla polskiego `1472`.

#### Czas propagacji
##### `chinadaily.com.cn`
* 32 bajty
```console
λ: ~$ ping -s 32 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 32 data bytes
40 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=423.866 ms
40 bytes from 124.127.180.200: icmp_seq=1 ttl=35 time=411.850 ms
40 bytes from 124.127.180.200: icmp_seq=2 ttl=35 time=466.810 ms
40 bytes from 124.127.180.200: icmp_seq=3 ttl=35 time=491.673 ms
40 bytes from 124.127.180.200: icmp_seq=4 ttl=35 time=501.233 ms
^C
--- chinadaily.com.cn ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 411.850/459.086/501.233/35.692 ms
```

Czas propagacji: `460 ms`

* 512 bajtów
```console
λ: ~$ ping -s 512 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 512 data bytes
520 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=435.069 ms
520 bytes from 124.127.180.200: icmp_seq=1 ttl=35 time=453.603 ms
520 bytes from 124.127.180.200: icmp_seq=2 ttl=35 time=477.460 ms
520 bytes from 124.127.180.200: icmp_seq=3 ttl=35 time=500.364 ms
520 bytes from 124.127.180.200: icmp_seq=4 ttl=35 time=521.615 ms
^C
--- chinadaily.com.cn ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 435.069/477.622/521.615/31.114 ms
```

Czas propagacji: `478 ms`

##### `onet.pl`
* 32 bajty
```console
λ: ~$ ping -D -s 32 onet.pl
PING onet.pl (213.180.141.140): 32 data bytes
40 bytes from 213.180.141.140: icmp_seq=0 ttl=59 time=16.088 ms
40 bytes from 213.180.141.140: icmp_seq=1 ttl=59 time=14.033 ms
40 bytes from 213.180.141.140: icmp_seq=2 ttl=59 time=14.218 ms
40 bytes from 213.180.141.140: icmp_seq=3 ttl=59 time=13.400 ms
40 bytes from 213.180.141.140: icmp_seq=4 ttl=59 time=13.595 ms
^C
--- onet.pl ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 13.400/14.267/16.088/0.957 ms
```

Czas propagacji: `14 ms`

* 512 bajtów
```console
λ: ~$ ping -D -s 512 onet.pl
PING onet.pl (213.180.141.140): 512 data bytes
520 bytes from 213.180.141.140: icmp_seq=0 ttl=59 time=14.211 ms
520 bytes from 213.180.141.140: icmp_seq=1 ttl=59 time=14.651 ms
520 bytes from 213.180.141.140: icmp_seq=2 ttl=59 time=15.751 ms
520 bytes from 213.180.141.140: icmp_seq=3 ttl=59 time=14.446 ms
520 bytes from 213.180.141.140: icmp_seq=4 ttl=59 time=15.459 ms
^C
--- onet.pl ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 14.211/14.904/15.751/0.597 ms
```

Czas propagacji: `15 ms`

Zaobserwowałem nieznaczny wzrost czasów propagacji, jednakże w obu przypadkach nie jest on znaczący i mieści się w granicy błędu.

### `traceroute`
```console
λ: ~$ traceroute chinadaily.com.cn
traceroute to chinadaily.com.cn (124.127.180.200), 64 hops max, 52 byte packets
 1  192.168.1.1 (192.168.1.1)  3.554 ms  1.589 ms  0.775 ms
 2  10.7.12.254 (10.7.12.254)  1.140 ms  1.997 ms  1.848 ms
(...)
18  be3142.ccr41.sjc03.atlas.cogentco.com (154.54.1.194)  184.843 ms
    be3144.ccr41.sjc03.atlas.cogentco.com (154.54.5.102)  187.738 ms  184.394 ms
19  38.104.139.250 (38.104.139.250)  422.068 ms  422.683 ms
    38.104.139.78 (38.104.139.78)  338.629 ms
20  * 202.97.50.61 (202.97.50.61)  243.705 ms  230.718 ms
21  202.97.90.249 (202.97.90.249)  392.110 ms  378.805 ms  421.396 ms
22  * 202.97.85.57 (202.97.85.57)  423.704 ms  467.748 ms
23  * * *
24  * * *
25  219.141.140.77 (219.141.140.77)  487.449 ms  412.323 ms *
26  bj141-163-165.bjtelecom.net (219.141.163.165)  422.619 ms *
    234.235.120.106.static.bjtelecom.net (106.120.235.234)  424.764 ms
27  * * *
28  * * 234.235.120.106.static.bjtelecom.net (106.120.235.234)  382.855 ms
29  * * *
30  * * *
(...)
53  * * *
54  * * *^C
```

Zaobserwowałem dużą ilość przeskoków pomiędzy routerami, po stronie ISP (hosty `*.atlas.cogentco.com`).

Poszukiwanie przerwałem po 54 przeskokach, co było liczbą znacznie przekraczającą wcześniej wyznaczone dane. Ogromna ilość przeskoków może być spowodowana topologią chińskiej sieci oraz nadzorowi nad tamtejszym ruchem sieciowym.

## `Wireshark`

Program Wireshark służy do obserwowania ruchu sieciowego, tzn. można zobaczyć zawartość pakietów wysyłanych i odbieranych przez komputer.