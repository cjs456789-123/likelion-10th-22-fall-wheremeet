const contentEle=document.getElementById('main');

const testContents = [
    {
        placeName: '경영관 2F 라운지',
        placePhoto: 'img/경영관2F라운지.png',
        placeKeyword: '#교내 #스터디/팀플 <br>#화상회의 <br>#움료/디저트 #야간',
        placeTime: '영업중',
        placeDistance: '440m',  
    },
    {
        placeName: '학생회관 라운지',
        placePhoto: 'img/학생회관라운지.png',
        placeKeyword: '#교내 #스터디/팀플 <br>#화상회의 <br>#움료/디저트 #야간',
        placeTime: '영업중',
        placeDistance: '440m',  
    },
    {
        placeName: '사랑방',
        placePhoto: 'img/사랑방.png',
        placeKeyword: '#교내 #스터디/팀플 <br>#화상회의 <br>#움료/디저트 #야간',
        placeTime: '영업중',
        placeDistance: '440m',  
    },
    {
        placeName: 'ttt',
        placePhoto: 'img/ttt.png',
        placeKeyword: '#교내 #스터디/팀플 <br>#화상회의 <br>#움료/디저트 #야간',
        placeTime: '영업중',
        placeDistance: '440m',  
    },
    
]

// 필터 값 따라서 할 수 있게 하면될까요?

const setContent = (contents) => {
    let contentsHTML = '';

    contents.forEach((content) => {
        contentsHTML +=  
        `
        <div class="content">
            <div>
                <h3 class="placeName">${content.placeName}</h3>
            </div>
            <div class="placePhoto">
                <img class="cafeimg" src="${content.placePhoto}" />
            </div>
            <div>
                <h5 class="placeKeyword">${content.placeKeyword}</h5>
            </div>
            <div>
                <h5 class="placeTime">${content.placeTime}</h5>
            </div>
            <div>
               <h6 class="placeDistance">${content.placeDistance}</h6> 
            </div>
        </div>
        `
    });

    contentEle.innerHTML = contentsHTML;
};

setContent(testContents);