# Convert an iTunes exported playlist into something
# readable (HTML list)
import sys, os, optparse, getopt
import re
import pandas as pd

# global (debug statements on)
debug = False

def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]

# If <> does not exist, adds it
# Generates </> to create end tag
# Usage:
#   ltype, end_ltype = parse_html("<ol>")
#   print ltype
#   print end_ltype
# Returns:
#   <ol>
#   </ol>
def clean_html_tag(tag):
    global debug

    is_contained = True # starts with '<', ends with '>'
    is_end_tag = True # user gave us a tag with '/' (end tag)

    clean_start_tag = ''
    clean_end_tag = ''

    parse_tag = find_between(tag,'<','>')
    clean_start_tag = '<' + parse_tag + '>'
    clean_end_tag = '</' + parse_tag + '>' 


    if debug:
        print 'The parsed html list tag (no <>): ',parse_tag
        print 'Clean start html tag: ',clean_start_tag
        print 'Clean end html tag: ',clean_end_tag

    return clean_start_tag, clean_end_tag


def clean_format_string(data,i,fmt):
    global debug
    rep = ('[Artist]', data['Artist'][i]),('[Name]', data['Name'][i]),('[Composer]',data['Composer'][i]),('[Album]',data['Album'][i]),('[Grouping]',data['Grouping'][i]),('[Genre]',data['Genre'][i]),('[Size]',data['Size'][i]),('[Time]',data['Time'][i]),('[Disc Number]',data['Disc Number'][i]),('[Disc Count]',data['Disc Count'][i]),('[Track Number]',data['Track Number'][i]),('[Track Count]',data['Track Count'][i]),('[Year]',data['Year'][i]),('[Date Modified]',data['Date Modified'][i]),('[Date Added]',data['Date Added'][i]),('[Bit Rate]',data['Bit Rate'][i]),('[Sample Rate]',data['Sample Rate'][i]),('[Volume Adjustment]',data['Volume Adjustment'][i]),('[Kind]',data['Kind'][i]),('[Equalizer]',data['Equalizer'][i]),('[Comments]',data['Comments'][i]),('[Plays]',data['Plays'][i]),('[Last Played]',data['Last Played'][i]),('[Skips]',data['Skips'][i]),('[Last Skipped]',data['Last Skipped'][i]),('[My Rating]',data['My Rating'][i]),('[Location]',data['Location'][i])
    return reduce(lambda a, kv: a.replace(*kv), rep, fmt)
            



# Main routine
def convert_playlist_to_html(ifile,ofile,ltype,etype,fmt):
    global debug

    output = open(ofile,"w")

    # Probably the most annoying thing, but it's necessary to hard-code
    # Otherwise, all sorts of jumbled stuff gets read out of order.
    colnames = ['Name','Artist','Composer','Album',
                'Grouping','Genre','Size','Time','Disc Number',
                'Disc Count','Track Number','Track Count',
                'Year','Date Modified','Date Added', 'Bit Rate',
                'Sample Rate','Volume Adjustment','Kind', 'Equalizer',
                'Comments','Plays', 'Last Played', 'Skips', 'Last Skipped',
                'My Rating', 'Location']

    # Read in a comma delim file (csv)
    data = pd.read_csv(ifile, 
                        delim_whitespace = False,
                        header = None,
                        names = colnames)
                     
    # Replace NaN with empty string so that we can write
    # the string to a file
    data.fillna('',inplace=True) 
    

    ltag, ltag_end = clean_html_tag(ltype)
    etag, etag_end = clean_html_tag(etype)

    # start html
    output.write(ltag)

    # write html data 
    for i in range(len(data)):
        output.write(etag)
        clean_track = clean_format_string(data,i,fmt)
        clean_track_str = str(clean_track)
        if(debug):
            print 'clean_format_string: ',clean_track_str
            continue
        output.write(clean_track_str)
        output.write(etag_end + "\n")

    # end html
    output.write(ltag_end)
    output.close()

# Used when --help or -h is used
def gen_help():
    print 'Default usage:\n\t playlist_to_html.py -i <inputfile> -o <outputfile>\n'
    print 'Output:'
    print '\t<ol>\n\t\t<li>Artist - Song Name</li>\n\t</ol>\n\n'
    print 'Specify outer list HTML (<ol>):\n\t playlist_to_html.py -i <inputfile> -o <outputfile> -l "<tag>"\n'
    print 'Output:'
    print '\t<tag>\n\t\t<li>Artist - Song Name</li>\n\t</tag>\n\n'
    print 'Specify inner element HTML (<li>):\n\t playlist_to_html.py -i <inputfile> -o <outputfile> -e "<tag>"\n'
    print 'Output:'
    print '\t<ol>\n\t\t<tag>Artist - Song Name</tag>\n\t</ol>\n\n'
    print 'Specify format string (must match iTunes playlist tag):'
    print '\tplaylist_to_html.py -i <inputfile> -o <outputfile> -f "[Artist] -> [Album] made [Name] : [Genre]"\n'
    print 'Output:'
    print '\t<ol>\n\t\t<li>Artist -> Album Name made Song Name : Genre Name</li>\n\t</ol>\n'
    print '\nIf debug information is wanted, please use "-d" or "--debug"'

# Used when --debug or -d is used
def gen_args_used(ifile,ofile,ltype,etype,fmt):
    print 'Arguments used: \n'
    print 'Input file: "', ifile,'"'
    print 'Output file: "', ofile,'"'
    print 'List type: ',ltype
    print 'Element type: ',etype
    print 'Format string: "',fmt,'"'

def main (argv):
    global debug
    list_type = '<ol>'      # default, ordered list, can be ul
    element_type = '<li>'   # default, list element can be li

    format_string = '[Artist] - [Name]' # default, these correspond to
                                    # different fields in the iTunes
                                    # generated file.

    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hdi:o:lef",["help","debug","ifile=","ofile=","list=","element=","fmt="])
    except getopt.GetoptError:
        print 'Incorrect usage, please try: playlist_to_html.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            gen_help()
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-l","--list"):
            list_type = arg
        elif opt in ("-e","--element"):
            element_type = arg
        elif opt in ("-f","--fmt"):
            format_string = arg

    # print debug info if specified by user
    if debug:
        gen_args_used(inputfile,outputfile,list_type,element_type,format_string)

    # Handle everything here
    convert_playlist_to_html(inputfile,outputfile,list_type,element_type,format_string)

if __name__ == '__main__':
    main(sys.argv[1:])
