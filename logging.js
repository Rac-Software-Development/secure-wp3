
function button() {
  $.ajax({
    cache: false,
    url: "http://127.0.0.1:5000/api/logging",
    method: "POST",
    dataType: "json",
    contentType: "application/json; charset=utf",
    success: function (data) {
      var text = ""
      for (var i = 0; i < data.length; i++) {
        text += data[i].id + "<br>"
      }

      $("#id").append(text);
      var text2 = ""
      for (var i = 0; i < data.length; i++) {
        text2 += data[i].ip + "<br>"
      }
      $("#ip").append(text2);
      var text3 = ""
      for (var i = 0; i < data.length; i++) {
        text3 += data[i].omgeving + "<br>"
      }
      $("#omg").append(text3);
      var text4 = ""
      for (var i = 0; i < data.length; i++) {
        text4 += data[i].tijdstip + "<br>"
      }
      $("#tijd").append(text4);
      var text5 = ""
      for (var i = 0; i < data.length; i++) {
        text5 += data[i].melding + "<br>"
      }
      $("#meld").append(text5);
      console.log(data);

    },
    error: function (xhr, status, errorthrown) {
      console.log("ERROR: " + errorthrown);
    }

  })
}