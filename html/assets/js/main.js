$( document ).ready(function() {

    amplifier={
      audio: {
        power: true,
        mute: false,
        volume: 0,
        bass: 0,
        treble: 0,
        state: 0,
        states: ["media", "music", "radio", "aux"],
        update: function(json) {
          this.power = json.power;
          this.mute = json.mute;
          this.volume = json.volume;
          this.bass = json.bass;
          this.treble = json.treble;
          this.state = json.state;
        }
      },
      setState: function (state) {
        this.state = state;
      },
      updateGui: function (state) {
        //console.log(amplifier);
        amplifier.updateNav(state);
        amplifier.updatePanel(state);
        amplifier.updateSliders(state);
        amplifier.showPanel(state);
      },
      updateNav: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv-press.png)');
            $("#btn-menu").css('background-image', 'url(/assets/images/menu.png)');
            $("#btn-music").css('background-image', 'url(/assets/images/menu-mp3.png)');
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio.png)'); 
            break;
          case "music":
            $("#btn-music").css('background-image', 'url(/assets/images/menu-mp3-press.png)');
            $("#btn-menu").css('background-image', 'url(/assets/images/menu.png)');
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv.png)');
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio.png)');  
            break;
          case "radio":
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio-press.png)');
            $("#btn-menu").css('background-image', 'url(/assets/images/menu.png)');
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv.png)');
            $("#btn-music").css('background-image', 'url(/assets/images/menu-mp3.png)');
            break;
          case "aux":
            $("#btn-aux").css("background: url('/assets/images/menu-press.png') no-repeat center");
            $("#btn-radio").css('background-image', 'url(/assets/images/menu-radio.png)');       
            $("#btn-media").css('background-image', 'url(/assets/images/menu-tv.png)');
            $("#btn-music").css('background-image', 'url(/assets/images/menu-mp3.png)');
            break;
        }
      },
      updatePanel: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            amplifier.media.updatePanel();       
            break;
          case "music":
            amplifier.music.updatePanel();  
            break;
          case "radio":
            amplifier.radio.updatePanel();
            break;
          case "aux":
            amplifier.aux.updatePanel();
            break;
          // case "off":
          //   amplifier.updatePanel("off");
        }
      },
      showPanel: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            $("#panel-tv").show();
            $("#panel-music").hide();
            $("#panel-menu").hide();
            $("#panel-radio").hide();            
            break;
          case "music":
            $("#panel-tv").hide();
            $("#panel-music").show();
            $("#panel-menu").hide();
            $("#panel-radio").hide();   
            break;
          case "radio":
            $("#panel-tv").hide();
            $("#panel-music").hide();
            $("#panel-menu").hide();
            $("#panel-radio").show();
            break;
          case "aux":
            $("#panel-tv").hide();
            $("#panel-music").hide();
            $("#panel-menu").show();
            $("#panel-radio").hide();
            break;
        }
      },
      updateSliders: function(state) {
        //console.log(state);
        switch(state) {
          case "media":
            var a = "#12aab2";
            var b = "#0bb";
            var c = "#055";
            break;
          case "music":
            var a = "#24ed24";
            var b = "#0b0";
            var c = "#050";
            break;
          case "radio":
            var a = "#d1ef22";
            var b = "#bb0";    
            var c = "#550";
            break;
          case "aux":
            var a = "#efefef";
            var b = "#bbb";    
            var c = "#555";
            break;
        }

        // Set Values      
        $("#vol-slider").val(this.audio.volume);
        $("#bass-slider").val(this.audio.bass);
        $("#treble-slider").val(this.audio.treble);

        // Set Colours
        $(".noUi-background").css("background", a);
        $(".noUi-handle").css("background", b);
        $(".noUi-handle").css('border', '4px solid ' + b).css('background-color', c);
      },
      init: function() {
          // Get current state of amp...
          // Show spinner while network connection is established
          // websocket connection?
          $.getJSON(amplifier.network.url + "get/all", function(json) {
            
            // Set button handlers
            amplifier.setupButtonHandlers();

            // Update State From Device
            amplifier.updateStateFromDevice(json);

            // Update the GUI
            amplifier.updateGui(json.state);

            // Start device refresh
            amplifier.network.init();
            amplifier.network.start();

          }).done(function(json) {
              //alert("success");
          }).fail(function(json) {
              amplifier.showNetworkFailed();
          }).always(function(json) {
              //alert("complete");
          });
      },
      updateStateFromDevice: function(json) {
          //console.log("current state of amp"); console.log(json); console.log(amplifier);
          // Aux
          amplifier.aux.update(json);
          // Audio
          amplifier.audio.update(json);
          // Radio
          amplifier.radio.update(json);
          // Mp3
          amplifier.music.update(json);
      },          
      setupButtonHandlers: function() {
        // Top Nav Button Handlers
        $("#btn-media").click(function(){ amplifier.selectMedia(); });
        $("#btn-music").click(function(){ amplifier.selectMusic(); });
        $("#btn-radio").click(function(){ amplifier.selectRadio(); });
        $("#btn-aux").click(function(){ amplifier.selectAux(); });

        // Main Control Sliders
        $("#vol-slider").noUiSlider({
          range: [0,100],
          start: [20,30],
          step: 1.58,
          handles: 1,
          slide: function() {
            amplifier.network.stop();
            $.get(amplifier.network.url + "set/volume/" + parseInt($(this).val()), function(amp) {
              amplifier.audio.volume = amp.volume
              amplifier.network.start();
            });
          }
        });
        $("#bass-slider").noUiSlider({
          range: [-14,14],
          start: [0,0],
          step: 2,
          handles: 1,
          slide: function() {
            amplifier.network.stop();
            $.get(amplifier.network.url + "set/bass/" + parseInt($(this).val()), function(amp) {
              amplifier.bass = amp.bass
              amplifier.network.start();
            });
          }
        });
        $("#treble-slider").noUiSlider({
          range: [-14,14],
          start: [0,0],
          step: 2,
          handles: 1,
          slide: function() {
            amplifier.network.stop();
            $.get(amplifier.network.url + "set/treble/" + parseInt($(this).val()), function(amp) {
              amplifier.treble = amp.treble
              amplifier.network.start();
            });
          }
        });
        
        // Radio Control
        $("#radio-prev").click(function(){ amplifier.radio.prev(); });
        $("#radio-next").click(function(){ amplifier.radio.next(); });

        // MP3 Control
        $("#mp3-list").click(function(){ amplifier.music.list(); });
        $("#mp3-repeat").click(function(){ amplifier.music.repeat(); });
        $("#mp3-prev").click(function(){ amplifier.music.prev(); });
        $("#mp3-play").click(function(){ amplifier.music.play(); });
        $("#mp3-next").click(function(){ amplifier.music.next(); });
        $("#mp3-shuffle").click(function(){ amplifier.music.shuffle(); });
        $("#mp3-playing").click(function(){ amplifier.music.playing(); });
      },
      showNetworkFailed: function () {
        // Show overlay
        $("body").mask("<p class='retry-spinner'/><p>Network Error...</p><p class='retry-now'><a class=\"retry-now-a\" href=\"javascript:location.reload();\">retry now</a></p>");        
      },
      selectMedia: function() {
        $.get(amplifier.network.url + "set/selectMedia", function(data) {
          amplifier.updateGui("media"); 
        });
      },
      selectMusic: function() {
        $.get(amplifier.network.url + "set/selectMusic", function(data) {          
          // Show song currently playing
          // mpd/index.php?cmd=getCurrentSong"
          $.getJSON(amplifier.network.url + "get/all", function(data) {
            //console.log(data)
            if (typeof data.mp3 === 'object') {
              amplifier.music.song.title = data.mp3.title;
              amplifier.music.song.artist = data.mp3.artist;                        
            } else {
              //console.log(data.mp3);
              amplifier.music.song.title = "server down";
              amplifier.music.song.artist = "server down";
              //console.log(amplifier.mp3);              
            }
            amplifier.updateGui("music");
            }).fail(function() {
              amplifier.music.song.title = "network error";
              amplifier.music.song.artist = "network error";
            })
        });
      },
      selectRadio: function() {
        $.get(amplifier.network.url + "set/selectRadio", function(data) {            
            amplifier.radio.updatePanel();
            amplifier.updateGui("radio");
        });
      },
      selectAux: function() {
        $.get(amplifier.network.url + "set/selectAux", function(data) {       
            amplifier.updateGui("aux");
        });
      },

      /**
       * Aux Object
       */
      aux: {
        update: function(json) {
        },
        updatePanel: function() {
          $("#info-volume").html("Volume: " + amplifier.audio.volume);
          $("#info-mute").html("Mute: " + amplifier.audio.mute);
          $("#info-treble").html("Treble: " + amplifier.audio.treble);
          $("#info-bass").html("Bass: " + amplifier.audio.bass);   
        }
      },

      /**
       * Network Object
       */
      network: {
        url: "http://" + window.location.hostname + "/",
        timer: null,
        delay: 7000,
        init: function() {
          window.clearTimeout(amplifier.network.timer);
        },
        start: function() {      
            //console.log("starting network timer");
            // Refresh Device Settings            
            $.getJSON(amplifier.network.url + "get/all", function(json) {                            
              amplifier.updateStateFromDevice(json);
              amplifier.updateGui(json.state);
              if(amplifier.network.timer == null) {
                amplifier.network.timer = setTimeout(function() {
                  amplifier.network.start()
                }, amplifier.network.delay);
              }
            }).fail(function(json) {
              amplifier.showNetworkFailed();              
            });           
          },
        stop: function() {
            //console.log("stopping network timer");
            window.clearTimeout(amplifier.network.timer);
            this.timer = null;
          }
      },

      /**
       * Media Object
       */
      media: {
        updatePanel: function() {
          this.clock.start();          
        },
        clock: {
          months: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          timer: null,     
          getTime: function (){
            var d = new Date();
            var month = d.getMonth();
            var day = d.getDate();
            return (day<10 ? '0' : '') + day + " " + this.months[d.getMonth()];
          },
          start: function(){
            this.show();          
            this.timer = setTimeout(function(){
              amplifier.media.clock.start()},
              500);
          },
          stop: function(){
            window.clearTimeout(this.timer);
          },
          show: function(){
            var d = new Date();
            $("#media-date").text(d.toDateString());
            $("#media-clock").text(d.toLocaleTimeString());
          }
        }
      },

      /**
       * Radio Object
       */
      radio: {
        station: {},   
        prev: function() {
          $.get(amplifier.network.url + "set/radioStationPrevious/", function(data) {
            amplifier.radio.station = data.radio;
            amplifier.radio.updatePanel();
          });
        },
        next: function() {          
          $.get(amplifier.network.url + "set/radioStationNext/", function(data) {
            amplifier.radio.station = data.radio;
            amplifier.radio.updatePanel();
          });
        },
        setByIndex: function(index) {          
          $.get(amplifier.network.url + "set/radioStationIndex/" + index, function(data) {
            amplifier.radio.station = data.radio;
            amplifier.radio.updatePanel();
          });
        },
        updatePanel: function() {
          $("#radio-frequency").text(amplifier.radio.station.frequency);
          $("#radio-name").text(amplifier.radio.station.name);
         },
        update: function(data) {
          amplifier.radio.station = data.radio;
        }
      },

      /**
       * Music Object
       */
      music: {
        volume:"0",
        playState: false,
        repeatState: false,
        shuffleState: false,
        playingState: false,
        currentlyPlaying: {},
        song: {
          "title": "",
          "artist": ""
        },
        update: function(json) {
          this.song = json.mp3;
        },
        list: function() {

        },
        toggleStr: function(bool) {
          if(bool == false)
            return "Off"
          return "On"
        },
        repeat: function() {
          amplifier.music.repeatState = !amplifier.music.repeatState;
          $.get(amplifier.network.url + "set/mp3Repeat" + amplifier.music.toggleStr(amplifier.music.repeatState), function(data) {
            amplifier.music.updatePanel(data);
          });
        },
        prev: function() {
          $.get(amplifier.network.url + "set/mp3Previous", function(data) {
            amplifier.music.updatePanel(data);
          });
        },
        play: function() {
          $.get(amplifier.network.url + "set/mp3Play", function(data) {
            amplifier.music.updatePanel(data);
          });
        },
        next: function() {
          $.get(amplifier.network.url + "set/mp3Next", function(data) {
            amplifier.music.updatePanel(data);
          });
        },
        shuffle: function() {
          amplifier.music.shuffleState = !amplifier.music.shuffleState;
          $.get(amplifier.network.url + "set/mp3Shuffle" + amplifier.music.toggleStr(amplifier.music.shuffleState), function(data) {
            amplifier.music.updatePanel(data);
          });
        },
        playing: function() {
          // Switch between playlist view and currently playing view
        },
        updatePanel: function() {
          var title = "Server error";
          var artist = "";
          if (typeof amplifier.music.song != 'undefined' && amplifier.music.song != false) {
            //console.log("song isn't false...");
            title = amplifier.music.song.title
            artist = amplifier.music.song.artist
          }
          $("#music-playing").html(title);
          $("#music-artist").html(artist);           
        }
      }     
    }
    // Initialise the main amplifier panel
    amplifier.init();
});
