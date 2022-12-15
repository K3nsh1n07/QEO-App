const btnDelete = document.querySelectorAll('.btn-delete')

if(btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            //Si hace click en cancelar o afuera, se ejecuta el prevent default
            if(!confirm('Estas seguro querer eliminar?')){
                e.preventDefault();
            }
        });
    });
}

obtenerMesa()
function obtenerMesa(){
    const queryString = window.location.search;

    const urlParams = new URLSearchParams(queryString);
    
    const page_type = urlParams.get('mesa')
    
    if (page_type){
        document.getElementById('idMesa').value = page_type
    }else{
        //Sin parametro el id default = caja
        document.getElementById('idMesa').value = 1
    }
    
}


function validarFormularioMenu(){
    var arr_cantidad = document.getElementsByName('iCantidad'); // array 
    let isValid = false;
   
    for (let index = 0; index < arr_cantidad.length; index++) {
        const element = arr_cantidad[index].value;
        if (element != 0) {
            isValid = true       
        }
        
    }

    if (isValid != true) {
        alert('Es necesario agregar alguna unidad para continuar.')
        return false
    }
   
}


function validarFormularioMedioPago(){

    var nombreCompleto = document.getElementById("tnombreCompleto").value;
    var rtelefono = new RegExp("^[0-9]+$");
    var telefono = document.getElementById("ttelefono").value;
    var email = document.getElementById("temail").value;
    if (nombreCompleto == "") {
        alert("Ingrese un Nombre válido");
        return false;
    }
    
    if (!rtelefono.test(telefono)) {
        alert("Ingrese solamente numeros: ej: 1133665522");
        return false;
    }

    if (email == "") {
        alert("Ingrese un Valor en el mail");
        return false;
    }
}
