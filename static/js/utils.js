//error message extraction

export function getErrorMessage(error) {
    if (typeof error.detail === "string"){
        return error.detail;
    } else if (Array.isArray(error.detail)){
        return error.detail.map((err)=> err.msg).join(". ");
    } 
    return "an error occurred, try again";
}

// display modal by id
export function showModal(modalID) {
    const modal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById(modalID)
    );
    modal.show();
    return modal;
}

// hide a bootstrap modal by ID
export function hideModal(modalID){
    const modal = bootstrap.Modal.getInstance(
        document.getElementById(modalID)
    );
    if (modal) modal.hide();
}