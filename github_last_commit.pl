#!/usr/bin/perl

use strict;
use JSON::XS;
my $a = '';
while (<>) { $a .= $_ }
my $d = decode_json $a;
print $d->{'commits'}[0]->{'id'};
