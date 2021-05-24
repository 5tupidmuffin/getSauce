// show a preview of the uploaded image

const config = {tools: ['crop']} // only enable crop
const ImageEditor = new FilerobotImageEditor(config);
var globalFile = document.getElementById('file')


var loadFile = function(event) {
    var output = document.getElementById('output');
    // console.log('files[0]: ' + event.target.files[0])
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
  };

function displayiamge(){
  setTimeout(function(){ LoadImageFromURL() }, 4)  // create delay to actually grab the link
}

function OpenImageEditor(){
  imagelink = document.getElementById("ImageLink").value;
  fileInput = document.getElementById('file')
  console.log('file:' + fileInput.value);
  
  if (fileInput.value != ""){
    if (fileInput.files[0] == undefined){
      window.alert("pasted images cannot be edited");
      return;
    }
    imageFile = fileInput.files[0]
    ImageEditor.open(imageFile);
  } else if (imagelink != ""){
    console.log('url block')
    ImageEditor.open(imagelink);
  } else {
    console.log('no media bolck')
    window.alert("what to edit ? upload image or provide image link")
  }

}


function duh(){ // called when clicking take me home on homepage
  window.alert("this is the Homepage duh");
}

function LoadImageFromURL(){
  imgop = document.getElementById("output");
  link = document.getElementById("ImageLink").value;
  console.log('img link ' + link)
  imgop.src = link;
  console.log(imgop.getAttribute('src'));
  }

/// upload image through CTRL+V ////
window.addEventListener('paste', e => {  
  fileInput = document.getElementById('file')
  fileInput.files = e.clipboardData.files;

  var output = document.getElementById('output');
  output.src = URL.createObjectURL(fileInput.files[0]);

  output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
  }
});


