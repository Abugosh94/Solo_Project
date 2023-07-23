$(document).click(function () {
    let filled = "M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
    let empty = "M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"
    $(".remFav").click(function () {
        $.ajax({
            url: '/test',
            type: 'GET',
            async: false,
            data: {
                button_text: $(this).text(),
                id: $("#id").text()
            },
            success: function (response) {
                console.log("rem")
                star = document.getElementById('star');
                star.setAttribute('d', empty);
                $(".remFav").text(response.text)
                $(".remFav").removeClass("remFav").addClass("addFav")
            }
        });
    });
    $(".addFav").click(function () {
        $.ajax({
            url: '/test',
            type: 'GET',
            async: false,
            data: {
                button_text: $(this).text(),
                id: $("#id").text()
            },
            success: function (response) {
                console.log("add")
                star = document.getElementById('star');
                star.setAttribute('d', filled);
                $(".addFav").text(response.text)
                $(".addFav").removeClass("addFav").addClass("remFav")
            }
        });
    });
});


$(document).ready(function () {
    $("#sort").on("change", function () {
        $.ajax({
            url: "sort_properties", // Replace with the actual URL for the sort_properties view
            type: "GET",
            data: {
                sort_id: $('#sort').val()
            },
            dataType: "json",
            success: function (data) { // On success, display the sorted properties
                displaySortedProperties(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log("Error:", errorThrown);
            }
        });
    });

    function displaySortedProperties(data) {
        var propertiesContainer = $("#properties-container");
        propertiesContainer.empty();

        // Loop through the sorted properties and update the HTML

        data.forEach(function (property) {
            var propertyDiv = $("<div>").addClass("col-md-4 properties");
            var cardBox = $("<div>").addClass("card-box-a card-shadow");
            var imgBox = $("<div>").addClass("img-box-a");

            // Image
            var imgSrc = property.id % 10 === 1 ? "static/img/property-" + property.id + ".jpg" : "static/img/property-" + property.id % 10 + ".jpg";
            var propertyImg = $("<img>").addClass("img-a img-fluid").attr("src", imgSrc);

            imgBox.append(propertyImg);

            // Card Overlay
            var cardOverlay = $("<div>").addClass("card-overlay");
            var cardOverlayContent = $("<div>").addClass("card-overlay-a-content");
            var cardHeader = $("<div>").addClass("card-header-a");
            var cardTitle = $("<h2>").addClass("card-title-a");
            var propertyLink = $("<a>").attr("href", "properties/" + property.id).html("<br /> " + property.city.toUpperCase());

            cardTitle.append(propertyLink);
            cardHeader.append(cardTitle);

            // Card Body
            var cardBody = $("<div>").addClass("card-body-a");
            var priceBox = $("<div>").addClass("price-box d-flex");
            var price = $("<span>").addClass("price-a").html((property.rent ? "Rent" : "Sale") + " | " + (
            property.currency === "usd" ? "$" : property.currency === "nis" ? "₪" : "JoD"
        ) + property.price);
            var propertyLink = $("<a>").addClass("link-a").attr("href", "properties/" + property.id).text("Click here to view");
            var arrowIcon = $("<span>").addClass("ion-ios-arrow-forward");

            priceBox.append(price);
            cardBody.append(priceBox, propertyLink, arrowIcon);

            // Card Footer
            var cardFooter = $("<div>").addClass("card-footer-a");
            var cardInfoList = $("<ul>").addClass("card-info d-flex justify-content-around");
            var areaItem = $("<li>").html("<h4 class='card-info-title'>Area</h4><span>" + property.area + "m<sup>2</sup></span>");
            var bedroomsItem = $("<li>").html("<h4 class='card-info-title'>Bedrooms</h4><span>" + property.beds + "</span>");
            var bathsItem = $("<li>").html("<h4 class='card-info-title'>Baths</h4><span>" + property.baths + "</span>");
            var garagesItem = $("<li>").html("<h4 class='card-info-title'>Garages</h4><span>" + property.garages + "</span>");

            cardInfoList.append(areaItem, bedroomsItem, bathsItem, garagesItem);
            cardFooter.append(cardInfoList);

            // Append card body and footer to the overlay content
            cardOverlayContent.append(cardHeader, cardBody, cardFooter);

            // Append overlay content to the card overlay
            cardOverlay.append(cardOverlayContent);

            // Append img box and card overlay to the card box
            cardBox.append(imgBox, cardOverlay);

            // Append the property div to the properties container
            propertyDiv.append(cardBox);

            // Append the property div to the properties container
            propertiesContainer.append(propertyDiv);
        });
    }
});