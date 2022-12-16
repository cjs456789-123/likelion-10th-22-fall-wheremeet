var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(37.5884546, 126.9926780), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

// if (navigator.geolocation) {
    
//     // GeoLocation을 이용해서 접속 위치를 얻어옵니다
//     navigator.geolocation.getCurrentPosition(function(position) {
        
//         var lat = position.coords.latitude, // 위도
//             lon = position.coords.longitude; // 경도
        
//         var locPosition = new kakao.maps.LatLng(lat, lon) // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
        
//         // 마커를 표시합니다
//         displayMarker(locPosition);
            
//     });
    
// } else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치를 설정합니다
    
//     var locPosition = new kakao.maps.LatLng(37.5884546, 126.9926780)
        
//     displayMarker(locPosition);
// }

function displayMarker(locPosition) {

    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({  
        map: map, 
        position: locPosition
    }); 
    
    // 지도 중심좌표를 접속위치로 변경합니다
    map.setCenter(locPosition);      
}    


var imageSrc = './img/marker.png', // 마커이미지의 주소입니다    
imageSize = new kakao.maps.Size(32, 32), // 마커이미지의 크기입니다
imageOption = {offset: new kakao.maps.Point(16, 40)}; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

// 마커가 표시될 위치입니다 
var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

// 마커를 클릭했을 때 해당 장소의 상세정보를 보여줄 커스텀오버레이입니다
var placeOverlay = new kakao.maps.CustomOverlay({zIndex:1}), 
    contentNode = document.createElement('div'), // 커스텀 오버레이의 컨텐츠 엘리먼트 입니다 
// 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다 
    positions = [
        {
            place_url: 'https://apis.map.kakao.com/web/sample/categoryFromBounds/',
            place_name: '경영관',
            open:'영업중',
            distance: '440m',
            latlng: new kakao.maps.LatLng(37.5884546, 126.9926780)
        },
        {
            place_url: 'https://apis.map.kakao.com/web/sample/categoryFromBounds/',
            place_name: '호암관',
            open:'영업중',
            distance: '440m',
            latlng: new kakao.maps.LatLng(37.5883551, 126.9920036)
        },
        {
            place_url: 'https://apis.map.kakao.com/web/sample/categoryFromBounds/',
            place_name: '국제관',
            open:'영업중',
            distance: '440m',
            latlng: new kakao.maps.LatLng(37.5867965, 126.9952135)
        },
        {
            place_url: 'https://apis.map.kakao.com/web/sample/categoryFromBounds/',
            place_name: '학생회관',
            open:'영업중',
            distance: '440m',
            latlng: new kakao.maps.LatLng(37.5874992, 126.9932746)
        }
    ];

// 커스텀 오버레이의 컨텐츠 노드에 css class를 추가합니다 
contentNode.className = 'placeinfo_wrap';

// 커스텀 오버레이의 컨텐츠 노드에 mousedown, touchstart 이벤트가 발생했을때
// 지도 객체에 이벤트가 전달되지 않도록 이벤트 핸들러로 kakao.maps.event.preventMap 메소드를 등록합니다 
addEventHandle(contentNode, 'mousedown', kakao.maps.event.preventMap);
addEventHandle(contentNode, 'touchstart', kakao.maps.event.preventMap);

// 커스텀 오버레이 컨텐츠를 설정합니다
placeOverlay.setContent(contentNode);  

// 엘리먼트에 이벤트 핸들러를 등록하는 함수입니다
function addEventHandle(target, type, callback) {
    if (target.addEventListener) {
        target.addEventListener(type, callback);
    } else {
        target.attachEvent('on' + type, callback);
    }
}

for (var i = 0; i < positions.length; i ++) {
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        map: map, // 마커를 표시할 지도
        position: positions[i].latlng, // 마커의 위치
        image: markerImage
    });
    // 마커와 검색결과 항목을 클릭 했을 때
    // 장소정보를 표출하도록 클릭 이벤트를 등록합니다
    (function(marker, position) {
        kakao.maps.event.addListener(marker, 'click', function() {
            displayPlaceInfo(position);
        });
    })(marker, positions[i]);
    
}

// 클릭한 마커에 대한 장소 상세정보를 커스텀 오버레이로 표시하는 함수입니다
function displayPlaceInfo (position) {
    var content = '<div class="placeinfo">' +
                    '   <a class="title" href="' + position.place_url + '" target="_blank" title="' + position.place_name + '">' + position.place_name + '</a>';      
    content += '    <span title="' + position.open + '">' + position.open + '</span>';

    content += '    <span class="distance">' + position.distance + '</span>' + 
                '</div>' + 
                '<div class="after"></div>';

    contentNode.innerHTML = content;
    placeOverlay.setPosition(position.latlng);
    placeOverlay.setMap(map);  
}


