document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    document.querySelector("#numbers").onchange = () => {
        var image_id = document.querySelector("#numbers").value
        if (document.querySelector("#image-source") == null) {
            var img = document.createElement("img");
            img.setAttribute("id", "image-source")
            document.querySelector("#image").appendChild(img);
        };

        var source = "static/collage/" + image_id + ".jpg"

        document.querySelector("#image-source").src = source;
        document.querySelector("#image-source").style.width = "800";

    };

});