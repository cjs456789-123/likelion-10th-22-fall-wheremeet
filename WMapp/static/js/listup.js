const filters=['1인', '2~4인', '5인 이상','원형','사각형', '창가석/벽좌석','좌식','콘센트','화상회의','미팅룸','흡연실']

const createFilterEle=(filter)=>{
    const filterEle=document.createElement("span");
    filterEle.classList.add('choice');
    const textEle=document.createTextNode(filter);
    filterEle.appendChild(textEle);
    return filterEle
};

const rootEle=document.getElementById('filter-container');

filters.forEach(filter => {
    const filterEle = createFilterEle(filter);
    rootEle.appendChild(filterEle);
})
