## A Prototype Web Based Monitoring Site Register For New Zealand.
The project aims to prototype a web based national monitoring site register for New Zealand, allowing the documentation and discovery of monitoring sites.  Sites will be able to be added by registered agencies, with an overall administration and governance function applying over all agencies.  The site will not provide measurement data, but will be able to provide links to the data.

## Further Information and Details.
The [Wiki](https://github.com/jeffcnz/mon-site-register/wiki) provides more information about the features and use of the api, an overview of conformance with the WFS 3 standard and more background and discussion on the implementation and related considerations.

## Motivation
The need for this kind of application has been identified as part of an environmental data infrastructure [Manaaki Whenua - Landcare Research 2018](https://www.landcareresearch.co.nz/__data/assets/pdf_file/0004/180796/Ritchie_2018_IDA_POC.pdf).  This infrastructure would aid in the realisation of services such as an environmental information brokering service [MfE 2017](https://www.mfe.govt.nz/sites/default/files/media/eidi_technical_report_2017.pdf) and environmental modelling and analysis [ELFIE](https://opengeospatial.github.io/ELFIE/).

An Envirolink report [Manaaki Whenua - Landcare Research 2017](http://www.envirolink.govt.nz/assets/Envirolink/1729-HZLC137-National-environmental-monitoring-site-identification2.pdf) proposed an identification system and describes the components of a register.  In order for the system to operate and be sustainable there need to be persistent url's for the sites, and a governance structure in place to administer the system.  This has resulted in a chicken and egg cycle where a register isn't created because there isn't a governance structure and a governance structure isn't created because there isn't anything to govern.  By demonstrating a web based site register it is hoped that this cycle can be broken.

## Implementation Considerations
The recomendations from the Envirolink report were used as guidance, however for this prototype the WMO WIGO Site Identifier has not been used.  Factors contributing to this decision were:-
1.  When implementing the database it was found that having multiple issuer identifiers added significant complexity to the scripting requirements.  Removing this requirement allowed out of the box functionality to be used.
2. 6 digit alphanumeric identifiers have the potential to spell words and could be confusing for human readers. eg a river flow site called soil1, or rain1, or any site being called bad12 etc.  Numeric identifiers avoid this and can be unlimited in number of sites, however their readability for humans will suffer when they are long.  Numeric identifiers are easier to implement (effectively out of the box).

Since the Envirolink report was published the OGC and W3C have published the OGCAPI-Features-Part 1: Core Standard [OGC 2019](https://github.com/opengeospatial/ogcapi-features).  While this defines the standard for a features API it appears to have many relevant aspects for a site register.
1. It recommends persistent, unique URI's.
2. It has the format {collection}/items/{identifier}, which is similar to components of the WMO WIGO Site identifier {series}{local-identifier}
3. It recommends linked data formats to facilitate reuse.
4. It relates to geographic features (sites).

This prototype aims to provide an OGCAPI Features compliant API service with a secure administration area for maintenence of the register.  The api can also allow for script based maintenence of sites (add and update) on a permissions basis.

[Spatial Data on the web best practices]{https://www.w3.org/TR/sdw-bp/#indexable-by-search-engines}

## Tech/framework used
<b>Built with</b>
- [Geo Django](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/)
- [PostGIS](https://postgis.net/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django REST Framework GIS](https://github.com/djangonauts/django-rest-framework-gis)
- [Bootstrap](https://getbootstrap.com/)

## Features  
- OGCAPI - Features compliant api (work in progress)
- Secure administration
- Browsable API with content negotiation
- Web based identifiers that could be easily registered to make them unique.
- Built using open source libraries.

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) © [Jeff Cooke]()
