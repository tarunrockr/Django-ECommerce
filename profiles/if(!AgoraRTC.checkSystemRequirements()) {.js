if(!AgoraRTC.checkSystemRequirements()) {
  alert("browser does not support webRTC");
}

/* select Log type */
// AgoraRTC.Logger.setLogLevel(AgoraRTC.Logger.NONE);
// AgoraRTC.Logger.setLogLevel(AgoraRTC.Logger.ERROR);
// AgoraRTC.Logger.setLogLevel(AgoraRTC.Logger.WARNING);
// AgoraRTC.Logger.setLogLevel(AgoraRTC.Logger.INFO);
// AgoraRTC.Logger.setLogLevel(AgoraRTC.Logger.DEBUG);

/* simulated data to proof setLogLevel() */
AgoraRTC.Logger.error('this is error');
AgoraRTC.Logger.warning('this is warning');
AgoraRTC.Logger.info('this is info');
AgoraRTC.Logger.debug('this is debug');

var client, localStream, camera, microphone;

var audioSelect = document.querySelector('select#audioSource');
var videoSelect = document.querySelector('select#videoSource');

function join() {
  document.getElementById("join").disabled = true;
  //document.getElementById("video").disabled = true;
  var channel_key = null;

  console.log("Init AgoraRTC client with vendor key: " + key.value);
  client = AgoraRTC.createClient({mode: 'live'});


  client.init(key.value, function () {
    console.log("AgoraRTC client initialized");
    client.join(channel_key, channel.value, null, function(uid) {
      console.log("User " + uid + " join channel successfully");

      camera = videoSource.value;
      microphone = audioSource.value;
      localStream = AgoraRTC.createStream({streamID: uid, audio: true, cameraId: camera, microphoneId: microphone, video: true, screen: false});
      //localStream = AgoraRTC.createStream({streamID: uid, audio: false, cameraId: camera, microphoneId: microphone, video: false, screen: true, extensionId: 'minllpmhdgpndnkomcoccfekfegnlikg'});
      if (document.getElementById("video").checked) {
        localStream.setVideoProfile('720p_3');

      }

      // The user has granted access to the camera and mic.
      localStream.on("accessAllowed", function() {
        console.log("accessAllowed");
      });

      // The user has denied access to the camera and mic.
      localStream.on("accessDenied", function() {
        console.log("accessDenied");
      });

      localStream.init(function() {
        console.log("getUserMedia successfully");
        localStream.play('agora_local');

        client.publish(localStream, function (err) {
          console.log("Publish local stream error: " + err);
        });

        client.on('stream-published', function (evt) {
          console.log("Publish local stream successfully");
           
           document.write(document.getElementById("iframe_id").contentWindow.location.href);
        });
      }, function (err) {
        console.log("getUserMedia failed", err);
      });
    }, function(err) {
      console.log("Join channel failed", err);
    });
  }, function (err) {
    console.log("AgoraRTC client init failed", err);
  });

  channelKey = "";
  client.on('error', function(err) {
    console.log("Got error msg:", err.reason);
    if (err.reason === 'DYNAMIC_KEY_TIMEOUT') {
      client.renewChannelKey(channelKey, function(){
        console.log("Renew channel key successfully");
      }, function(err){
        console.log("Renew channel key failed: ", err);
      });
    }
  });


  client.on('stream-added', function (evt) {
    var stream = evt.stream;
    console.log("New stream added: " + stream.getId());
    console.log("Subscribe ", stream);
    client.subscribe(stream, function (err) {
      console.log("Subscribe stream failed", err);
    });
  });

  client.on('stream-subscribed', function (evt) {
    var stream = evt.stream;
    console.log("Subscribe remote stream successfully: " + stream.getId());
    if ($('div#video #agora_remote'+stream.getId()).length === 0) {
      $('div#video').append('<div id="agora_remote'+stream.getId()+'" style="float:left; width:810px;height:607px;display:inline-block;"></div>');
    }
    stream.play('agora_remote' + stream.getId());
  });

  client.on('stream-removed', function (evt) {
    var stream = evt.stream;
    stream.stop();
    $('#agora_remote' + stream.getId()).remove();
    console.log("Remote stream is removed " + stream.getId());
  });

  client.on('peer-leave', function (evt) {
    var stream = evt.stream;
    if (stream) {
      stream.stop();
      $('#agora_remote' + stream.getId()).remove();
      console.log(evt.uid + " leaved from this channel");
    }
  });
}

function leave() {
  document.getElementById("leave").disabled = true;
  client.leave(function () {
    console.log("Leavel channel successfully");
  }, function (err) {
    console.log("Leave channel failed");
  });
}


function muteAudio()
{
  document.getElementById("unmuteAudio").disabled = false;
  document.getElementById("muteAudio").disabled = true;
  //localStream.disableAudio();
 localStream.disableAudio();
}
function unmuteAudio()
{
  document.getElementById("unmuteAudio").disabled = true;
  document.getElementById("muteAudio").disabled = false;
 localStream.enableAudio();
}

function enableVideo()
{
  document.getElementById("disableVideo").disabled = false;
  document.getElementById("enableVideo").disabled = true;
  localStream.enableVideo();

}
function disableVideo()
{
  document.getElementById("disableVideo").disabled = true;
  document.getElementById("enableVideo").disabled = false;
  localStream.disableVideo();
}

function getDevices() {
  AgoraRTC.getDevices(function (devices) {
    for (var i = 0; i !== devices.length; ++i) {
      var device = devices[i];
      var option = document.createElement('option');
      option.value = device.deviceId;
      if (device.kind === 'audioinput') {
        option.text = device.label || 'microphone ' + (audioSelect.length + 1);
        audioSelect.appendChild(option);
      } else if (device.kind === 'videoinput') {
        option.text = device.label || 'camera ' + (videoSelect.length + 1);
        videoSelect.appendChild(option);
      } else {
        console.log('Some other kind of source/device: ', device);
      }
    }
  });
}

//audioSelect.onchange = getDevices;
//videoSelect.onchange = getDevices;
getDevices();