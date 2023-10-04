#!/usr/bin/env ruby
puts ARGV[0].scan(/(Google)|(\+?\d{11})|(-1:0:-1:0:-1)/).join
