$("#deleteSTModal").on('show.bs.modal', function(e){
    $("#stid").val(e.relatedTarget.dataset.stid)
    $("#delete_modal_post").attr("action", e.relatedTarget.dataset.postUrl)
})
