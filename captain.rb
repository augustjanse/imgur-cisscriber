require 'open-uri'
require 'meme_captain'

template = ARGV[0]
top = ARGV[1]
bottom = ARGV[2]

f = open(template, 'rb')
i = MemeCaptain.meme_top_bottom(f, top, bottom)
i.write('out.jpg')
