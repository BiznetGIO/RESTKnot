var hex_chr = "0123456789abcdef";
function rhex(num)
{
  str = "";
  for(j = 0; j <= 3; j++)
    str += hex_chr.charAt((num >> (j * 8 + 4)) & 0x0F) +
           hex_chr.charAt((num >> (j * 8)) & 0x0F);
  return str;
}


function str2blks_MD5(str)
{
  nblk = ((str.length + 8) >> 6) + 1;
  blks = new Array(nblk * 16);
  for(i = 0; i < nblk * 16; i++) blks[i] = 0;
  for(i = 0; i < str.length; i++)
    blks[i >> 2] |= str.charCodeAt(i) << ((i % 4) * 8);
  blks[i >> 2] |= 0x80 << ((i % 4) * 8);
  blks[nblk * 16 - 2] = str.length * 8;
  return blks;
}


function add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}


function rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}


function cmn(q, a, b, x, s, t)
{
  return add(rol(add(add(a, q), add(x, t)), s), b);
}
function ff(a, b, c, d, x, s, t)
{
  return cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function gg(a, b, c, d, x, s, t)
{
  return cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function hh(a, b, c, d, x, s, t)
{
  return cmn(b ^ c ^ d, a, b, x, s, t);
}
function ii(a, b, c, d, x, s, t)
{
  return cmn(c ^ (b | (~d)), a, b, x, s, t);
}


function calcMD5(str)
{
  x = str2blks_MD5(str);
  a =  1732584193;
  b = -271733879;
  c = -1732584194;
  d =  271733878;

  for(i = 0; i < x.length; i += 16)
  {
    olda = a;
    oldb = b;
    oldc = c;
    oldd = d;

    a = ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = ff(c, d, a, b, x[i+10], 17, -42063);
    b = ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = ff(d, a, b, c, x[i+13], 12, -40341101);
    c = ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = ff(b, c, d, a, x[i+15], 22,  1236535329);    

    a = gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = gg(c, d, a, b, x[i+11], 14,  643717713);
    b = gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = gg(c, d, a, b, x[i+15], 14, -660478335);
    b = gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = gg(b, c, d, a, x[i+12], 20, -1926607734);
    
    a = hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = hh(b, c, d, a, x[i+14], 23, -35309556);
    a = hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = hh(d, a, b, c, x[i+12], 11, -421815835);
    c = hh(c, d, a, b, x[i+15], 16,  530742520);
    b = hh(b, c, d, a, x[i+ 2], 23, -995338651);

    a = ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = ii(c, d, a, b, x[i+10], 15, -1051523);
    b = ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = ii(d, a, b, c, x[i+15], 10, -30611744);
    c = ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = ii(b, c, d, a, x[i+ 9], 21, -343485551);

    a = add(a, olda);
    b = add(b, oldb);
    c = add(c, oldc);
    d = add(d, oldd);
  }
  return rhex(a) + rhex(b) + rhex(c) + rhex(d);
}

function addSOADefault(domain_id, domain_name){
    var d = new Date();
    var zone_id = domain_name;
        zone_id = calcMD5(domain_name+d)
        var json_zone={
            "insert": {
               "fields": {
                    "zone_name": domain_name,
                    "domain_id": domain_id
               },
               "tags": {
                   "zone_id": zone_id
               }
            }
         }

        var request = $.ajax({
            url:"http://127.0.0.1:6968/api/zone",
            type:"POST",
            data: JSON.stringify(json_zone),
            contentType:"application/json",
            dataType:"json",
            success: function(respon){
                var record_data_id = calcMD5(domain_name+"_soa");
                json_data_record={
                    "insert": {
                       "fields": {
                            "record_data_name": domain_name,
                            "type_name_id": "1",
                            "zone_id": zone_id
                       },
                       "tags": {
                           "record_data_id": record_data_id
                       }
                           
                    }
                 }

                 var request = $.ajax({
                    url:"http://127.0.0.1:6968/api/datarecord",
                    type:"POST",
                    data: JSON.stringify(json_data_record),
                    contentType:"application/json",
                    dataType:"json",
                    success: function(respon){
                        var ttl_data_id = record_data_id+"_ttl"
                        ttl_data_id = calcMD5(ttl_data_id)
                        json_ttl_data={
                            "insert": {
                               "fields": {
                                 "record_data_id": record_data_id,
                                 "ttl_id": "1"
                               },
                               "tags": {
                                   "ttl_data_id": ttl_data_id
                               }
                            }
                        }
                        var request3 = $.ajax({
                            url:"http://127.0.0.1:6968/api/datattl",
                            type:"POST",
                            data: JSON.stringify(json_ttl_data),
                            contentType:"application/json",
                            dataType:"json",
                            success: function(respon){
                                var content_id = record_data_id+"_ctn_ns1"
                                content_id = calcMD5(content_id)
                                var content_id_soa_default = content_id
                                json_content={
                                    "insert": {
                                       "fields": {
                                            "content_name": "ns1.biz.net.id.",
                                            "ttl_data_id": ttl_data_id
                                       },
                                       "tags": {
                                           "content_id": content_id
                                       }
                                    }
                                 }

                                var request1 = $.ajax({
                                    url:"http://127.0.0.1:6968/api/content",
                                    type:"POST",
                                    data: JSON.stringify(json_content),
                                    contentType:"application/json",
                                    dataType:"json",
                                    success: function(respon){
                                        var content_id_data = record_data_id+"_ctn_data_10800"
                                        content_id_data = calcMD5(content_id_data)
                                        json_content_data10800={
                                            "insert": {
                                               "fields": {
                                                   "content_data_name": "10800",
                                                    "content_data_date": "2018070410",
                                                    "content_id": content_id
                                               },
                                               "tags": {
                                                   "content_data_id" : content_id_data
                                               }
                                            }
                                         }
                                         
                                        var request4 = $.ajax({
                                            url:"http://127.0.0.1:6968/api/datacontent",
                                            type:"POST",
                                            data: JSON.stringify(json_content_data10800),
                                            contentType:"application/json",
                                            dataType:"json",
                                            success: function(respon){
                                                console.log("OK")
                                            }
                                        });

                                        request4.done(function(msg){
                                            return true;
                                        });
                                        request4.fail(function( jqXHR, textStatus ) {
                                            return false;
                                        });

                                        var content_id_data = record_data_id+"_ctn_data_3600"
                                        content_id_data = calcMD5(content_id_data)
                                         json_content_data3600={
                                             "insert": {
                                                 "fields": {
                                                     "content_data_name": "3600",
                                                     "content_data_date": "2018070410",
                                                     "content_id": content_id
                                                 },
                                                 "tags": {
                                                     "content_data_id" : content_id_data
                                                 }
                                             }
                                         }

                                        var request5 = $.ajax({
                                            url:"http://127.0.0.1:6968/api/datacontent",
                                            type:"POST",
                                            data: JSON.stringify(json_content_data3600),
                                            contentType:"application/json",
                                            dataType:"json",
                                            success: function(respon){
                                                console.log("OK")
                                            }
                                        });

                                        request5.done(function(msg){
                                            return true;
                                        });
                                        request5.fail(function( jqXHR, textStatus ) {
                                            return false;
                                        });

                                        var content_id_data = record_data_id+"_ctn_data_604800"
                                        content_id_data=calcMD5(content_id_data)
                                         json_content_data604800={
                                             "insert": {
                                                 "fields": {
                                                     "content_data_name": "604800",
                                                     "content_data_date": "2018070410",
                                                     "content_id": content_id
                                                 },
                                                 "tags": {
                                                     "content_data_id" : content_id_data
                                                 }
                                             }
                                         }

                                        var request6 = $.ajax({
                                            url:"http://127.0.0.1:6968/api/datacontent",
                                            type:"POST",
                                            data: JSON.stringify(json_content_data604800),
                                            contentType:"application/json",
                                            dataType:"json",
                                            success: function(respon){
                                                console.log("OK")
                                            }
                                        });
                                        request6.done(function(msg){
                                            return true;
                                        });
                                        request6.fail(function( jqXHR, textStatus ) {
                                            return false;
                                        });

                                        var content_id_data = record_data_id+"_ctn_data_38400"
                                        content_id_data=calcMD5(content_id_data)
                                        json_content_data38400={
                                             "insert": {
                                                 "fields": {
                                                     "content_data_name": "38400",
                                                     "content_data_date": "2018070410",
                                                     "content_id": content_id
                                                 },
                                                 "tags": {
                                                     "content_data_id" : content_id_data
                                                 }
                                             }
                                        }
                                        

                                        var request7 = $.ajax({
                                            url:"http://127.0.0.1:6968/api/datacontent",
                                            type:"POST",
                                            data: JSON.stringify(json_content_data38400),
                                            contentType:"application/json",
                                            dataType:"json",
                                            success: function(respon){
                                                console.log("OK TERAKHIR")
                                                var soa_sync = {
                                                    "zone-soa-insert": {
                                                       "tags": {
                                                           "zone_id" : zone_id,
                                                           "ttl_data_id": ttl_data_id,
                                                           "content_id": content_id_soa_default
                                                       }
                                                    }
                                                }
                                                console.log(soa_sync)
                                                
                                                var sycn_soa = $.ajax({
                                                    url:"http://127.0.0.1:6968/api/sendcommand",
                                                    type:"POST",
                                                    data: JSON.stringify(soa_sync),
                                                    contentType:"application/json",
                                                    dataType:"json",
                                                    success: function(respon){
                                                        console.log("SOA SYNCS")
                                                    }
                                                });
                                            }
                                        });
                                        request7.done(function(msg){
                                            return true;
                                        });
                                        request7.fail(function( jqXHR, textStatus ) {
                                            return false;
                                        });
                                    }
                                });
                                request1.done(function(msg){
                                    return true
                                });
                                request1.fail(function( jqXHR, textStatus ) {
                                    return true
                                });
                                var content_id_hs1 = record_data_id+"_ctn_hs1"
                                content_id_hs1 = calcMD5(content_id_hs1)
                                json_content_hs1={
                                    "insert": {
                                       "fields": {
                                            "content_name": "hostmaster.biz.net.id.",
                                            "ttl_data_id": ttl_data_id
                                       },
                                       "tags": {
                                           "content_id": content_id_hs1
                                       }
                                    }
                                 }
                                var request2 =  $.ajax({
                                    url:"http://127.0.0.1:6968/api/content",
                                    type:"POST",
                                    data: JSON.stringify(json_content_hs1),
                                    contentType:"application/json",
                                    dataType:"json",
                                    success: function(respon){
                                        return true
                                    }
                                });
                                request2.done(function(msg){
                                    return true
                                });
                                request2.fail(function( jqXHR, textStatus ) {
                                    return false
                                });
                                
                            }
                        });
                        request3.done(function(msg){
                           return true
                        });
                        request3.fail(function( jqXHR, textStatus ) {
                            return false
                        });
                    }
                });
                request.done(function(msg){
                    
                    return true;
                });
                request.fail(function( jqXHR, textStatus ) {
                    return false;
                });
            }
        });
        return request
}


function addNSDefault(domain_id, domain_name, ns_name){
    var d = new Date();
    var zone_id = domain_name;
        zone_id = calcMD5(zone_id+d)
        var json_zone={
            "insert": {
               "fields": {
                    "zone_name": domain_name,
                    "domain_id": domain_id
               },
               "tags": {
                   "zone_id": zone_id
               }
            }
         }

        var a = $.ajax({
            url:"http://127.0.0.1:6968/api/zone",
            type:"POST",
            data: JSON.stringify(json_zone),
            contentType:"application/json",
            dataType:"json",
            success: function(respon){
                var record_data_id = domain_name+"_ns"+ns_name
                record_data_id = calcMD5(record_data_id)
                json_data_record={
                    "insert": {
                       "fields": {
                            "record_data_name": domain_name,
                            "type_name_id": "5",
                            "zone_id": zone_id
                       },
                       "tags": {
                           "record_data_id": record_data_id
                       }
                           
                    }
                 }

                 var req = $.ajax({
                    url:"http://127.0.0.1:6968/api/datarecord",
                    type:"POST",
                    data: JSON.stringify(json_data_record),
                    contentType:"application/json",
                    dataType:"json",
                    success: function(respon){
                        var ttl_data_id = record_data_id+"_ttl"+ns_name
                        ttl_data_id=calcMD5(record_data_id)
                        json_ttl_data={
                            "insert": {
                               "fields": {
                                 "record_data_id": record_data_id,
                                 "ttl_id": "1"
                               },
                               "tags": {
                                   "ttl_data_id": ttl_data_id
                               }
                            }
                        }
                        var req = $.ajax({
                            url:"http://127.0.0.1:6968/api/datattl",
                            type:"POST",
                            data: JSON.stringify(json_ttl_data),
                            contentType:"application/json",
                            dataType:"json",
                            success: function(respon){
                                var content_id = record_data_id+"_ctn"+ns_name
                                content_id = calcMD5(content_id)
                                json_content={
                                    "insert": {
                                       "fields": {
                                            "content_name": ns_name,
                                            "ttl_data_id": ttl_data_id
                                       },
                                       "tags": {
                                           "content_id": content_id
                                       }
                                    }
                                 }

                                var req = $.ajax({
                                    url:"http://127.0.0.1:6968/api/content",
                                    type:"POST",
                                    data: JSON.stringify(json_content),
                                    contentType:"application/json",
                                    dataType:"json",
                                    success: function(respon){
                                        console.log("NS INSERTED")
                                        var json_ns_sycn={
                                            "zone-ns-insert": {
                                               "tags": {
                                                    "record_data_id" : record_data_id,
                                                    "ttl_data_id": ttl_data_id
                                               }
                                            }
                                        }
                                        var rea_sycn_ns = $.ajax({
                                            url:"http://127.0.0.1:6968/api/sendcommand",
                                            type:"POST",
                                            data: JSON.stringify(json_ns_sycn),
                                            contentType:"application/json",
                                            dataType:"json",
                                            success: function(respon){
                                                console.log("NS SYNC")
                                            }
                                        });
                                    }
                                });

                                req.done(function(msg){
                                    return true;
                                });
                                req.fail(function( jqXHR, textStatus ) {
                                    return textStatus;
                                });
                            }
                        });
                        req.done(function(msg){
                            return true;
                        });
                        req.fail(function( jqXHR, textStatus ) {
                            return textStatus;
                        });
                    }
                });
                req.done(function(msg){
                    console.log(msg)
                    return true
                });
                req.fail(function( jqXHR, textStatus ) {
                    return textStatus;
                });
            }
        });
        return a;
}
$(document).ready(function(){
    rule_content = [
        {
            "id" : 3,
            "content": 1,
            "serial": 3,
            "name": "srv"
        },
        {
            "name": "A",
            "content":1,
            "serial": 0,
            "id": 2
        },
        {
            "name": "cname",
            "content": 1,
            "serial":0,
            "id" : 4
        }
    ]

    $('#typename_id').change(function(){
        $("#serial_content_section").html("");
        $('#jns_record').val("")
        var typesname = $('#typename_id').val()
        for (a=0; a < rule_content.length; a++){
            if (typesname == rule_content[a].id){
                $('#jns_record').val(rule_content[a].name)
                for (i=1; i <= rule_content[a].content; i++){
                    var data = '<div class="form-group"><label>Serial Data</label><input type="text" class="form-control" id="content_name_'+i+'" /></div>'
                    $("#serial_content_section").append(data);
                    if(rule_content[a].serial > 0){
                        for(c=1; c <= rule_content[a].serial; c++){
                           var data_serial = '<div class="form-group"><label>Serial Data</label><input type="text" class="form-control" id="content_data_serial'+c+'" /></div>'
                           $("#serial_data_content_section").append(data);
                        }
                    }
                }
            }
        }
    });

    $('#btnAddRecord').click(function(){
        var a = $('#jns_record').val()
        console.log(a)
    });


    $('#btnCreateDomain').click(function(){
        var d = new Date();
        var domain_name = $("#domain_value").val();
        var domain_id = $("#domain_value").val();
        domain_id = calcMD5(domain_id+d)
        var json_domain = {
            "insert": {
               "fields": {
                   "domain_name": domain_name
               },
               "tags": {
                   "domain_id": domain_id
               }
                   
            }
         }
        $.ajax({
            url:"http://127.0.0.1:6968/api/domain",
            type:"POST",
            data: JSON.stringify(json_domain),
            contentType:"application/json",
            dataType:"json",
            success: function(respon){
                return 1
            }
        });

        var json_domain_insert_agent = {
            "conf-insert": {
               "tags": {
                   "domain_id" : domain_id
               }
            }
        }

        var conf_insert = $.ajax({
            url:"http://127.0.0.1:6968/api/sendcommand",
            type:"POST",
            data: JSON.stringify(json_domain_insert_agent),
            contentType:"application/json",
            dataType:"json",
            success: function(respon){
                return 1
            }
        });

        synctoagent = conf_insert.done(function(msg){
            console.log(domain_name+" Inserted To Agen : "+msg)
        })

        soa = addSOADefault(domain_id, domain_name)
        c = soa.done(function(msg){
            console.log("soa save: "+msg)
        })
        ns1 = addNSDefault(domain_id, domain_name, "ns1.biz.net.id.")
        a = ns1.done(function(msg){
            console.log("ns1 save: "+msg)
        })
        ns2 = addNSDefault(domain_id, domain_name, "hostmaster.biz.net.id.")
        b = ns2.done(function(msg){
            console.log("ns2 save: "+msg)
        })


    });

    $('#record_section').hide();

    $.ajax({
        url: 'http://127.0.0.1:6968/api/zone',
        dataType: 'json',
        success: function(resp) {
            var table = $('#domain_table').DataTable({
                "select": true,
                "data": resp.data.data,
                "columns": [
                    { "data": "domain_id",},
                    { "data": "zone_id" },
                    { "data": "zone_name" },
                    { "data": "time" }
                ],
            });
            $('#domain_table tbody').on( 'click', 'tr', function (e) {
                $('#record_section').show()
                $('#record_table').html("")
                var data = table.row(this).data();
                json_data = {
                    "where": {
                       "tags": {
                           "zone_id": data.zone_id
                       }
                    }
                 }
                 $("#zone_f_id").val(data.zone_id)
                 $.ajax({
                    url:"http://127.0.0.1:6968/api/datarecord",
                    type:"POST",
                    data: JSON.stringify(json_data),
                    contentType:"application/json",
                    dataType:"json",
                    success: function(respon){
                        // $("record_table tbody").load(respon.data.data);
                        var $thead = $('<thead>').append(
                            $('<tr>').append(
                                $('<td>').text("Record ID"),
                                $('<td>').text("Record Name"),
                                $('<td>').text("Zone ID"),
                                $('<td>').text("Type Name ID"),
                                $('<td>').text("Time")
                            )
                        );
                        $('#record_table').append($thead)
                        tbody = $("<tbody>")
                        $.each(respon.data.data, function(i, item) {
                            var tr = $('<tr>').append(
                                $('<td>').text(item.record_data_id),
                                $('<td>').text(item.record_data_name),
                                $('<td>').text(item.zone_id),
                                $('<td>').text(item.type_name_id),
                                $('<td>').text(item.time)
                            );
                            tbody.append(tr)
                        });
                        // console.log(tbody)
                        $('#record_table').append(tbody)

                        $.ajax({
                            url:"http://127.0.0.1:6968/api/typename",
                            type:"GET",
                            success: function(respon){
                                var data = $.map(respon.data.data, function (obj) {
                                    obj.id = obj.type_name_id;
                                    obj.text = obj.type_name; 
                                    return obj;
                                });
                                $('#typename_id').select2({
                                    data : data
                                });
                            }
                        });


                        $.ajax({
                            url:"http://127.0.0.1:6968/api/ttl",
                            type:"GET",
                            success: function(respon){
                                var data = $.map(respon.data.data, function (obj) {
                                    obj.id = obj.ttl_id;
                                    obj.text = obj.ttl_name; 
                                    return obj;
                                });
                                $('#ttl_id_name').select2({
                                    data : data
                                });
                            }
                        });
                    }
                  });
            });
        }
    });
});