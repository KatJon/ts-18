use HTTP::Daemon;
use HTTP::Response;
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