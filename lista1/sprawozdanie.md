# Technologie sieciowe - Lista 1
## Zadanie 1
Przetestuj działanie programów:
### `ping`
> Komendy wykorzystane przeze mnie różnią się od standardowych, ze względu na system operacyjny (macOS), w którym występuje `ping` w wersji z rodziny BSD
* `chinadaily.com.cn` (Pekin)
    + `-m ttl` TTL
    + `-D` flaga "Nie fragmentuj"
    + `-s n` rozmiar pakietu 

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
* Odległość: `64 - 35 = 29 przeskoków` 

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

A więc maksymalna wielkość niefragmentowanego pakietu wynosi dla chińskiego hosta `997`, a dla polskiego `1472`.

#### Czas propagacji
##### `chinadaily.com.cn`
* 32 bajty
```console
λ: ~$ ping -s 32 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 32 data bytes
40 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=408.826 ms
```

Czas propagacji: `409 ms`

* 512 bajtów
```console
λ: ~$ ping -s 512 chinadaily.com.cn
PING chinadaily.com.cn (124.127.180.200): 512 data bytes
520 bytes from 124.127.180.200: icmp_seq=0 ttl=35 time=480.805 ms
```

Czas propagacji: `481 ms`

##### `onet.pl`
* 32 bajty
```console
λ: ~$ ping -s 32 onet.pl
PING onet.pl (213.180.141.140): 32 data bytes
40 bytes from 213.180.141.140: icmp_seq=0 ttl=59 time=13.932 ms
```

Czas propagacji: `14 ms`

* 512 bajtów
```console
λ: ~$ ping -s 512 onet.pl
PING onet.pl (213.180.141.140): 512 data bytes
520 bytes from 213.180.141.140: icmp_seq=0 ttl=59 time=19.526 ms
```