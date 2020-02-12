$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test', {transports:['websocket']});

    socket.on('connect', function() {
                socket.emit('client_connect', {'data': 'I\'m connected!'});
            });
    $('form').submit(function(){
    socket.emit('form submit', {'stop':$('#stops').val(), 'direction':$('#direction').val()});
    return false;
    });
    //receive details from server
    socket.on('trip_updates', function(msg) {
        var updt = ''
        _update = msg.update;
        console.log('Update received')
        for (line in _update) {
          if (["A", "C", "E"].includes(line)){
            updt += '<div class="line"><span class="mta-ace mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["B", "D", "F", "M"].includes(line)){
            updt += '<div class="line"><span class="mta-bdfm mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["G"].includes(line)){
            updt += '<div class="line"><span class="mta-g mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["J", "Z"].includes(line)){
            updt += '<div class="line"><span class="mta-jz mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["L"].includes(line)){
            updt += '<div class="line"><span class="mta-l mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["N", "Q", "R"].includes(line)){
            updt += '<div class="line"><span class="mta-nqr mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["S"].includes(line)){
            updt += '<div class="line"><span class="mta-s mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["1", "2", "3"].includes(line)){
            updt += '<div class="line"><span class="mta-123 mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["4", "5", "6"].includes(line)){
            updt += '<div class="line"><span class="mta-456 mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          else if (["7"].includes(line)){
            updt += '<div class="line"><span class="mta-7 mta-bullet">' + line + '</span>'
            updt += '<div class="minutes_blocks">'
            for (time in _update[line]){
              updt += '<div class="minute_block"><span class="mta">' + _update[line][time] + '</span><br><span class="minutes">min</span></div>'
            }
            updt += '<br></div></div>'
          }
          };
        $('#updt').html(updt)
      });

    });
