def create_virtual_tour_object(data, property):
    from decimal import Decimal
    from properties.models import Link, Marker, HotspotNode, VirtualTour

    virtual_tour = VirtualTour.objects.create(
        property=property,
        defaultViewPosition_latitude=Decimal(data["defaultViewPosition"].get("latitude")),
        defaultViewPosition_longitude=Decimal(data["defaultViewPosition"].get("longitude")),
        initialView=data.get("initialView", None)
    )

    nodes = []
    for node in data.get("hotspotNodes"):

        hotspot_node = HotspotNode.objects.create(
            id=node.get("id"),
            panorama="/home/nati/Desktop/1674411002858.jpeg",
            virtual_tour=virtual_tour
        )

        links = []
        for link in node.get("links", []):
            _link = Link.objects.create(
                nodeId=link.get("nodeId"),
                latitude=Decimal(link.get("latitude")),
                longitude=Decimal(link.get("longitude")),
                node=hotspot_node
            )

            links.append(_link)

        hotspot_node.links.set(links)

        markers = []
        for marker in node.get("markers", []):
            _marker = Marker.objects.create(
                id=marker.get("id", ""),
                linksTo=marker.get("linksTo"),
                tooltip=marker.get("tooltip", ""),
                width=marker.get("width"),
                height=marker.get("height"),
                longitude=Decimal(marker.get("longitude")),
                latitude=Decimal(marker.get("longitude")),
                anchor=marker.get("anchor"),
                node=hotspot_node
            )

            markers.append(_marker)

        hotspot_node.markers.set(markers)
        
        nodes.append(hotspot_node)    
    
    virtual_tour.hotspotNodes.set(nodes)

    return virtual_tour