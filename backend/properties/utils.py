def create_virtual_tour_object(data, imgs, property):
    from decimal import Decimal
    from properties.models import Link, Marker, HotspotNode, VirtualTour
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage
    from django.utils.text import get_valid_filename
    import os
    import uuid
    import imghdr
    import base64

    default_view_position = (data["defaultViewPosition"]) 
    virtual_tour = VirtualTour.objects.create(
        property=property,
        defaultViewPosition_latitude=Decimal(default_view_position.get("latitude")),
        defaultViewPosition_longitude=Decimal(default_view_position.get("longitude")),
        initialView=data.get("initialView", None)
    )

    nodes = []
    hotspot_nodes = (data.get("hotspotNodes"))

    for node in hotspot_nodes:


        # extension
        base64_data = imgs.get(node.get("id"))
        format, imgstr = base64_data.split(";base64,")
        ext = format.split("/")[-1]
        unique_filename = str(uuid.uuid4())
        image = ContentFile(base64.b64decode(imgstr), name=f"{unique_filename}.{ext}")

        hotspot_node = HotspotNode.objects.create(
            id=node.get("id"),
            panorama=image,
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
                latitude=Decimal(marker.get("latitude")),
                anchor=marker.get("anchor"),
                node=hotspot_node
            )

            markers.append(_marker)

        hotspot_node.markers.set(markers)
        
        nodes.append(hotspot_node)    
    
    virtual_tour.hotspotNodes.set(nodes)

    return virtual_tour


def calculate_rating(ratings):
    sum = 0
    total = ratings.count()

    if total == 0:
        return 0.0

    for rating in ratings:
        sum += rating.rating

    return sum/total