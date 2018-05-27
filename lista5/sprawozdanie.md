Lista 5 - Szymon Wróbel
===

Zadanie 1
---
> Uruchom ten skrypt, przetestuj, zastanów się jak działa.

Wprowadziłem kilka poprawek ułatwiających uruchomienie skryptu:
* dodanie atrybutu `Reuse`, pozwalającego na ponowne wykorzystanie gniazda
* rozwinięcie skrótowych nazw ($c ==> $connection)
* wypisanie żądanego URI
* zmiana ścieżki odsyłanego pliku

```perl
use HTTP::Daemon;
use HTTP::Status;  

my $daemon = HTTP::Daemon->new(
        LocalAddr => 'localhost',
        LocalPort => 5000,
        Reuse => 1,
    ) || die;

print "Server running at: ", $daemon->url, "\n";

while (my $connection = $daemon->accept) {
    while (my $request = $connection->get_request) {
        if ($request->method eq 'GET') {
            print "GET ", $request->uri, "\n";
            $file_s= "page/index.html";
            $connection->send_file_response($file_s);
        }
        else {
            $connection->send_error(RC_FORBIDDEN)
        }
    }
    $connection->close;
    undef($connection);
}
```

Skrypt ten jest prostym serwerem HTTP, odpowiadającym na żądania GET i zwracający wtedy plik `page/index.html`, w przeciwnym razie zwraca błąd `403 Forbidden`

Zadanie 2
---
> Nawiąż połączenie za pomocą przykładowych klientów z listy poprzedniej.

Nieaktualne

Zadanie 3
---
> Nawiąż połączenie za pomocą przeglądarki internetowej.

Pomyślnie udało się nawiązać połączenie z serwerem i uzyskać dostęp do zasobu.

Zadanie 4
---

> Zmień skrypt (lub napisz własny serwer w dowolnym języku programowania) tak aby wysyłał do klienta nagłówek jego żądania.

Skrypt z zadania 4 jest modyfikacją oryginalnego skryptu

```perl
while (my $connection = $daemon->accept) {
    while (my $request = $connection->get_request) {
        if ($request->method eq 'GET') {
            print "GET ", $request->uri, "\n";
            my $payload = $request->as_string;
            my $response = HTTP::Response->new(200);
            $response->header("Content-Type" => "text/text");
            $response->content($payload);
            $connection->send_response($response);
        }
        else {
            $connection->send_error(RC_FORBIDDEN);
        }
    }
    $connection->close;
    undef($connection);
}
```

W odpowiedzi na żądanie GET tworzę odpowiedź `200 OK` oraz ustawiam typ MIME odpowiedzi na `text/text`. Zawartością odpowiedzi jest treść żądania w formie napisu.

Po przygotowaniu, odpowiedź jest odsyłana do klienta.

Zadanie 5
---

> Zmień skrypt (lub napisz własny serwer w dowolnym języku programowania) tak aby obsugiwał żądania klienta do prostego tekstowego serwisu WWW (kilka statycznych ston z wzajemnymi odwołaniami) zapisanego w pewnym katalogu dysku lokalnego komputera na którym uruchomiony jest skrypt serwera.

Ustaliłem, że folderem głównym strony będzie katalog `page`. Jego struktura jest następująca:

```text
page
  |  index.html
  |  p1.html
  |  p2.html
```

Skrypt jest modyfikacją oryginalnego skryptu:

```perl
while (my $request = $connection->get_request) {
    if ($request->method eq 'GET') {
        my $uri = $request->uri;
        print "GET ", $uri, "\n";

        if ($uri eq "/") {
            $uri = "/index.html";
        }

        my $requested_file = "page" . $uri;

        if ( -e $requested_file) {
            $connection->send_file_response($requested_file);
        } else {
            $connection->send_error(RC_NOT_FOUND);
        }
    }
    else {
        $connection->send_error(RC_FORBIDDEN)
    }
}
```

W przypadku, gdy odwołujemy się do głównego folderu ścieżka jest ustalana jako ścieżka strony głównej (`index.html`).

Następnie tworzę ścieżkę do zasobu, a potem sprawdzam, czy zasób istnieje. W wypadku istnienia zasobu jest on wysyłany, a w przeciwnym razie odsyłana jest odpowiedź `404 Not Found`.

Zadanie 6
---

Korzystałem z programu `Wireshark`. W moim przypadku ruch odbywał się na urządzeniu lo0.

Przeglądarka na porcie: 52784
Serwer na porcie: 5000

#### Żądanie wysłane z przeglądarki:
```
0000   02 00 00 00 45 02 02 50 00 00 40 00 40 06 00 00  ....E..P..@.@...
0010   7f 00 00 01 7f 00 00 01 ce 30 13 88 ee b9 5c fd  .........0....\.
0020   30 b9 45 ea 80 18 31 d7 00 45 00 00 01 01 08 0a  0.E...1..E......
0030   66 7b 7e 94 66 7b 7e 94 47 45 54 20 2f 69 6e 64  f{~.f{~.GET /ind
0040   65 78 2e 68 74 6d 6c 20 48 54 54 50 2f 31 2e 31  ex.html HTTP/1.1
0050   0d 0a 48 6f 73 74 3a 20 31 32 37 2e 30 2e 30 2e  ..Host: 127.0.0.
0060   31 3a 35 30 30 30 0d 0a 43 6f 6e 6e 65 63 74 69  1:5000..Connecti
0070   6f 6e 3a 20 6b 65 65 70 2d 61 6c 69 76 65 0d 0a  on: keep-alive..
0080   43 61 63 68 65 2d 43 6f 6e 74 72 6f 6c 3a 20 6d  Cache-Control: m
0090   61 78 2d 61 67 65 3d 30 0d 0a 55 70 67 72 61 64  ax-age=0..Upgrad
00a0   65 2d 49 6e 73 65 63 75 72 65 2d 52 65 71 75 65  e-Insecure-Reque
00b0   73 74 73 3a 20 31 0d 0a 55 73 65 72 2d 41 67 65  sts: 1..User-Age
00c0   6e 74 3a 20 4d 6f 7a 69 6c 6c 61 2f 35 2e 30 20  nt: Mozilla/5.0 
00d0   28 4d 61 63 69 6e 74 6f 73 68 3b 20 49 6e 74 65  (Macintosh; Inte
00e0   6c 20 4d 61 63 20 4f 53 20 58 20 31 30 5f 31 33  l Mac OS X 10_13
00f0   5f 31 29 20 41 70 70 6c 65 57 65 62 4b 69 74 2f  _1) AppleWebKit/
0100   35 33 37 2e 33 36 20 28 4b 48 54 4d 4c 2c 20 6c  537.36 (KHTML, l
0110   69 6b 65 20 47 65 63 6b 6f 29 20 43 68 72 6f 6d  ike Gecko) Chrom
0120   65 2f 36 36 2e 30 2e 33 33 35 39 2e 31 37 30 20  e/66.0.3359.170 
0130   53 61 66 61 72 69 2f 35 33 37 2e 33 36 0d 0a 41  Safari/537.36..A
0140   63 63 65 70 74 3a 20 74 65 78 74 2f 68 74 6d 6c  ccept: text/html
0150   2c 61 70 70 6c 69 63 61 74 69 6f 6e 2f 78 68 74  ,application/xht
0160   6d 6c 2b 78 6d 6c 2c 61 70 70 6c 69 63 61 74 69  ml+xml,applicati
0170   6f 6e 2f 78 6d 6c 3b 71 3d 30 2e 39 2c 69 6d 61  on/xml;q=0.9,ima
0180   67 65 2f 77 65 62 70 2c 69 6d 61 67 65 2f 61 70  ge/webp,image/ap
0190   6e 67 2c 2a 2f 2a 3b 71 3d 30 2e 38 0d 0a 52 65  ng,*/*;q=0.8..Re
01a0   66 65 72 65 72 3a 20 68 74 74 70 3a 2f 2f 31 32  ferer: http://12
01b0   37 2e 30 2e 30 2e 31 3a 35 30 30 30 2f 70 32 2e  7.0.0.1:5000/p2.
01c0   68 74 6d 6c 0d 0a 41 63 63 65 70 74 2d 45 6e 63  html..Accept-Enc
01d0   6f 64 69 6e 67 3a 20 67 7a 69 70 2c 20 64 65 66  oding: gzip, def
01e0   6c 61 74 65 2c 20 62 72 0d 0a 41 63 63 65 70 74  late, br..Accept
01f0   2d 4c 61 6e 67 75 61 67 65 3a 20 65 6e 2d 47 42  -Language: en-GB
0200   2c 65 6e 3b 71 3d 30 2e 39 2c 65 6e 2d 55 53 3b  ,en;q=0.9,en-US;
0210   71 3d 30 2e 38 2c 70 6c 3b 71 3d 30 2e 37 0d 0a  q=0.8,pl;q=0.7..
0220   49 66 2d 4d 6f 64 69 66 69 65 64 2d 53 69 6e 63  If-Modified-Sinc
0230   65 3a 20 53 75 6e 2c 20 32 37 20 4d 61 79 20 32  e: Sun, 27 May 2
0240   30 31 38 20 31 34 3a 34 31 3a 33 38 20 47 4d 54  018 14:41:38 GMT
0250   0d 0a 0d 0a                                      ....
```

#### Odpowiedzi serwera:

Kod odpowiedzi:
```
0000   02 00 00 00 45 02 00 45 00 00 40 00 40 06 00 00  ....E..E..@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 45 ea  ...........00.E.
0020   ee b9 5f 19 80 18 31 c6 fe 39 00 00 01 01 08 0a  .._...1..9......
0030   66 7b 7e a6 66 7b 7e 94 48 54 54 50 2f 31 2e 31  f{~.f{~.HTTP/1.1
0040   20 32 30 30 20 4f 4b 0d 0a                        200 OK..
```

Nagłówek daty:
```
0000   02 00 00 00 45 02 00 59 00 00 40 00 40 06 00 00  ....E..Y..@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 45 fb  ...........00.E.
0020   ee b9 5f 19 80 18 31 c6 fe 4d 00 00 01 01 08 0a  .._...1..M......
0030   66 7b 7e a6 66 7b 7e a6 44 61 74 65 3a 20 53 75  f{~.f{~.Date: Su
0040   6e 2c 20 32 37 20 4d 61 79 20 32 30 31 38 20 31  n, 27 May 2018 1
0050   35 3a 30 39 3a 35 36 20 47 4d 54 0d 0a           5:09:56 GMT..
```

Typ serwera:
```
0000   02 00 00 00 45 02 00 55 00 00 40 00 40 06 00 00  ....E..U..@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 46 20  ...........00.F 
0020   ee b9 5f 19 80 18 31 c6 fe 49 00 00 01 01 08 0a  .._...1..I......
0030   66 7b 7e a6 66 7b 7e a6 53 65 72 76 65 72 3a 20  f{~.f{~.Server: 
0040   6c 69 62 77 77 77 2d 70 65 72 6c 2d 64 61 65 6d  libwww-perl-daem
0050   6f 6e 2f 36 2e 30 31 0d 0a                       on/6.01..
```

Typ MIME odpowiedzi:
```
0000   02 00 00 00 45 02 00 4d 00 00 40 00 40 06 00 00  ....E..M..@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 46 41  ...........00.FA
0020   ee b9 5f 19 80 18 31 c6 fe 41 00 00 01 01 08 0a  .._...1..A......
0030   66 7b 7e a6 66 7b 7e a6 43 6f 6e 74 65 6e 74 2d  f{~.f{~.Content-
0040   54 79 70 65 3a 20 74 65 78 74 2f 68 74 6d 6c 0d  Type: text/html.
0050   0a                                               .
```

Długość odpowiedzi:
```
0000   02 00 00 00 45 02 00 49 00 00 40 00 40 06 00 00  ....E..I..@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 46 5a  ...........00.FZ
0020   ee b9 5f 19 80 18 31 c6 fe 3d 00 00 01 01 08 0a  .._...1..=......
0030   66 7b 7e a6 66 7b 7e a6 43 6f 6e 74 65 6e 74 2d  f{~.f{~.Content-
0040   4c 65 6e 67 74 68 3a 20 34 34 34 0d 0a           Length: 444..
```

Data ostatniej modyfikacji:
```
0000   02 00 00 00 45 02 00 62 00 00 40 00 40 06 00 00  ....E..b..@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 46 6f  ...........00.Fo
0020   ee b9 5f 19 80 18 31 c6 fe 56 00 00 01 01 08 0a  .._...1..V......
0030   66 7b 7e a7 66 7b 7e a6 4c 61 73 74 2d 4d 6f 64  f{~.f{~.Last-Mod
0040   69 66 69 65 64 3a 20 53 75 6e 2c 20 32 37 20 4d  ified: Sun, 27 M
0050   61 79 20 32 30 31 38 20 31 34 3a 34 31 3a 33 38  ay 2018 14:41:38
0060   20 47 4d 54 0d 0a                                 GMT..
```

Zawartość odpowiedzi:
```
0000   02 00 00 00 45 02 01 f0 00 00 40 00 40 06 00 00  ....E.....@.@...
0010   7f 00 00 01 7f 00 00 01 13 88 ce 30 30 b9 46 9f  ...........00.F.
0020   ee b9 5f 19 80 18 31 c6 ff e4 00 00 01 01 08 0a  .._...1.........
0030   66 7b 7e a7 66 7b 7e a7 3c 21 44 4f 43 54 59 50  f{~.f{~.<!DOCTYP
0040   45 20 68 74 6d 6c 3e 0a 3c 68 74 6d 6c 3e 0a 3c  E html>.<html>.<
0050   68 65 61 64 3e 0a 20 20 20 20 3c 6d 65 74 61 20  head>.    <meta 
0060   63 68 61 72 73 65 74 3d 22 75 74 66 2d 38 22 20  charset="utf-8" 
0070   2f 3e 0a 20 20 20 20 3c 6d 65 74 61 20 68 74 74  />.    <meta htt
0080   70 2d 65 71 75 69 76 3d 22 58 2d 55 41 2d 43 6f  p-equiv="X-UA-Co
0090   6d 70 61 74 69 62 6c 65 22 20 63 6f 6e 74 65 6e  mpatible" conten
00a0   74 3d 22 49 45 3d 65 64 67 65 22 3e 0a 20 20 20  t="IE=edge">.   
00b0   20 3c 74 69 74 6c 65 3e 4c 69 73 74 61 20 35 3c   <title>Lista 5<
00c0   2f 74 69 74 6c 65 3e 0a 20 20 20 20 3c 6d 65 74  /title>.    <met
00d0   61 20 6e 61 6d 65 3d 22 76 69 65 77 70 6f 72 74  a name="viewport
00e0   22 20 63 6f 6e 74 65 6e 74 3d 22 77 69 64 74 68  " content="width
00f0   3d 64 65 76 69 63 65 2d 77 69 64 74 68 2c 20 69  =device-width, i
0100   6e 69 74 69 61 6c 2d 73 63 61 6c 65 3d 31 22 3e  nitial-scale=1">
0110   0a 3c 2f 68 65 61 64 3e 0a 3c 62 6f 64 79 3e 0a  .</head>.<body>.
0120   20 20 20 20 3c 68 31 3e 4c 69 73 74 61 20 35 3c      <h1>Lista 5<
0130   2f 68 31 3e 0a 20 20 20 20 3c 68 32 3e 4d 61 69  /h1>.    <h2>Mai
0140   6e 3c 2f 68 32 3e 0a 20 20 20 20 3c 75 6c 3e 0a  n</h2>.    <ul>.
0150   20 20 20 20 20 20 20 20 3c 6c 69 3e 3c 61 20 68          <li><a h
0160   72 65 66 3d 22 69 6e 64 65 78 2e 68 74 6d 6c 22  ref="index.html"
0170   3e 4d 61 69 6e 3c 2f 61 3e 3c 2f 6c 69 3e 0a 20  >Main</a></li>. 
0180   20 20 20 20 20 20 20 3c 6c 69 3e 3c 61 20 68 72         <li><a hr
0190   65 66 3d 22 70 31 2e 68 74 6d 6c 22 3e 50 61 67  ef="p1.html">Pag
01a0   65 20 31 3c 2f 61 3e 3c 2f 6c 69 3e 0a 20 20 20  e 1</a></li>.   
01b0   20 20 20 20 20 3c 6c 69 3e 3c 61 20 68 72 65 66       <li><a href
01c0   3d 22 70 32 2e 68 74 6d 6c 22 3e 50 61 67 65 20  ="p2.html">Page 
01d0   32 3c 2f 61 3e 3c 2f 6c 69 3e 0a 20 20 20 20 3c  2</a></li>.    <
01e0   2f 75 6c 3e 0a 3c 2f 62 6f 64 79 3e 0a 3c 2f 68  /ul>.</body>.</h
01f0   74 6d 6c 3e                                      tml>
```