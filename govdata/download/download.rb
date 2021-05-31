require "net/http"
require "json"
require "csv"
require "date"
require 'fileutils'

BASE_URL = "https://ckan.govdata.de/api/3/action"

class Download
  def save_package_ids(directory = ".")
    ids_url = "#{BASE_URL}/package_list"
    uri = URI(ids_url)
    response = Net::HTTP.get(uri)
    ids = JSON.parse(response)

    File.open("#{directory}/packages.json","w") do |f|
      f.write(response)
    end
    ids["result"]
  end

  def save_rdf(package_id)
    filename = "#{package_id}.rdf"
    date = DateTime.now.strftime("%Y%m%d")
    file_path = "packages/#{date}/#{filename}"
    unless File.file?(file_path)
      url = "https://www.govdata.de/ckan/dataset/#{package_id}.rdf"
      uri = URI(URI.encode(url))
      response = Net::HTTP.get(uri)
      File.open(file_path,"w") do |f|
        f.write(response)
      end
    end
  end

  def run
    date = DateTime.now.strftime("%Y%m%d")
    directory = "packages/#{date}"
    unless File.directory?(directory)
      FileUtils.mkdir_p directory
    end
    ids = save_package_ids(directory)
    ids.each do |id|
      save_rdf(id)
    end
  end
end

if $PROGRAM_NAME == __FILE__
  d = Download.new
  d.run
end
