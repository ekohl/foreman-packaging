#!/usr/bin/env ruby
require 'nokogiri'

def print_usage
  usage = <<-USAGE
add_to_comps - adds packagereqs for a package to a comps xml file

Usage ./add_to_comps.rb comps-file package-name [nonscl]

Examples:
  ./add_to_comps.rb comps/comps-foreman-rhel7.xml nodejs-example
  ./add_to_comps.rb comps/comps-foreman-rhel7.xml nodejs-example nonscl

Return codes:

  0 - successfully added
  1 - package is already present
  2 - wrong arguments
USAGE
  puts usage
end

def find_packagereq(comps, package_name)
  comps.xpath('//packagelist/packagereq').select { |s| s.text == package_name }
end

# Gets subset of packagereqs that are not -docs nor comments
def get_packagereqs(packagelist)
  relevant = []
  packagelist.children.each do |packagereq|
    # Break as soon as you find a comment which means start
    # of nonscl packages or start of -doc packages
    break if packagereq.class == Nokogiri::XML::Comment
    relevant << packagereq
    packagereq.unlink
  end
  relevant
end

def prepend_packagereqs(packagelist, packagereqs)
  if packagelist.children.empty?
    # If empty, we can add them alphabetically
    packagereqs.sort { |x,y| x.text <=> y.text }.each do |packagereq|
      packagelist << packagereq
    end
  else
    # Otherwise prepend them in reverse order
    packagereqs.sort { |x,y| y.text <=> x.text }.each do |packagereq|
      packagelist.prepend_child(packagereq)
    end
  end
end

if ![2, 3].include?(ARGV.length) ||
    ARGV.length == 3 && ARGV[2] != 'nonscl'
  print_usage
  exit(2)
end

comps = Nokogiri::XML(File.open(ARGV[0])) { |config| config.noblanks }
exit(1) unless find_packagereq(comps, ARGV[1]) == []
packagelist = comps.xpath("//packagelist").first

new_packagereq = Nokogiri::XML::Node.new 'packagereq', comps
new_packagereq['type'] = 'default'
new_packagereq.content = ARGV[1]

if ARGV[2] == 'nonscl'
  # Strip out SCL packages
  scl_packagereqs = get_packagereqs(packagelist)

  # Strip out non-SCL packages
  nonscl_comment = packagelist.children.shift
  if nonscl_comment
    nonscl_comment.unlink
    nonscl_packagereqs = get_packagereqs(packagelist)
    # At this point, only -doc packages remain
    nonscl_packagereqs << new_packagereq
    # Readd non-SCL packages
    prepend_packagereqs(packagelist, nonscl_packagereqs)
    packagelist.children.before(nonscl_comment)
  else
    # There was no non-SCL section
    # At this point, only -doc packages remain
    scl_packagereqs << new_packagereq
  end

  # Readd SCL-packages
  prepend_packagereqs(packagelist, scl_packagereqs)
else
  packagereqs = get_packagereqs(packagelist)
  packagereqs << new_packagereq
  prepend_packagereqs(packagelist, packagereqs)
end

File.write(ARGV[0], comps.to_xml)
exit 0
