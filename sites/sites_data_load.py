


from wfs_read import emarWfsRead






def missingCheck(key, dict):
	if key in dict:
		return dict[key]
	else:
		return None


error = 0

def load_lawa_site(wfs_url, tempagency):
	url = wfs_url#w['sites_url']
	print "Reading " + url
	sitesinfo = emarWfsRead(url)
	print str(len(sitesinfo)) + " Sites in WFS"
	for site in sitesinfo:
		#print site['CouncilSiteID']
		# Check if the site is already in the database

		# Check if there's a siteID
		site_id = missingCheck('councilsiteid', site)
		if site_id:
			#site_id = missingCheck('SiteID', site)
			if newSite != None:
				#site is in database.  Add to conflicts list, don't load

				newSite.site_name = site_id
				newSite.agency = tempagency
				newSite.latlng = missingCheck('latlong', site)
				newSite.latitude = missingCheck('latitude', site)
				newSite.longitude = missingCheck('longitude', site)

				newSite.description = missingCheck('description', site)




			else:
				# Load new site
				newSite = MonitoringSites(
					national_id = missingCheck('lawasiteid', site),
					site_name = site_id,
					agency = tempagency,
					latlng = missingCheck('latlong', site),
					latitude = missingCheck('latitude', site),
					longitude = missingCheck('longitude', site),


				
		else:
			error += 1

	print str(error) + " Sites not imported"
