function previewFile(obj,targetID){
    var fileData = new FileReader();
    fileData.onload = (function() {
      //id属性が付与されているimgタグのsrc属性に、fileReaderで取得した値の結果を入力することで
      //プレビュー表示している
      document.getElementById(targetID).src = fileData.result;
    });
    fileData.readAsDataURL(obj.files[0]);
    const formData = new FormData();
    formData.append("avatar", fileData.result);
  }

function hiddenElem(elem) {
  var id = document.getElementById(elem);
  id.style.display = "none";
}
