$(document).ready(function () {
    // Keep the server's order (grouped by time slot); search box comes with DataTables
    $('#timeConflictsTable').DataTable({
        paging: false,
        order: []
    });
});
