const schoolLounge = [
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
    
]

const schoolCafe = [
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

function createContainerEle (category, contents) {
  const containerEle = document.createElement("div");

  const categoryEle = createCategoryEle(category);
  const contentsEle = createContentsEle(contents);

  containerEle.appendChild(categoryEle);
  containerEle.appendChild(contentsEle);  

  return containerEle;
}

const createCategoryEle=(categoryName)=>{
    const categoryEle = document.createElement("h3");
    categoryEle.classList.add('category');
    const textEle = document.createTextNode(categoryName);
    categoryEle.appendChild(textEle);
    return categoryEle
};

const createContentsEle = (contents) => {
    const contentEle = document.createElement('div');
    contentEle.classList.add('mainContent');
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
    return contentEle;
}

const mainEle = document.getElementById('main');
const containerEle1 = createContainerEle('교내라운지', schoolLounge);
const containerEle2 = createContainerEle('교내카페', schoolCafe);

mainEle.appendChild(containerEle1);
mainEle.appendChild(containerEle2);