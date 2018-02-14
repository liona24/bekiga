import { urlApi } from './urls.js';
const $ = require('jquery');

function postFlaw(flaw) {
    return new Promise(function(resolve) {
        let pictureType = flaw.pictureFile ? flaw.pictureFile.name.split('.').pop() : null;
        let formData = new FormData();
        formData.append('flaw', flaw.flaw);
        formData.append('notes', flaw.notes);
        formData.append('priority', flaw.priority);
        formData.append('picture', pictureType);

        $.ajax({
            type: 'POST',
            url: urlApi + 'flaws/',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: (resp) => {
                let _id = resp.result._id;
                console.log('FLAW SUBMITTED - ID=' + _id);
                flaw._id = _id;

                if (pictureType) {
                    let pictureForm = new FormData();
                    pictureForm.append('pic', flaw.pictureFile);
                    pictureForm.append('_id', 'flaw_' + _id + '.' + pictureType);
                    $.ajax({
                        url : urlApi + 'files/',
                        data: pictureForm,
                        contentType: false,
                        cache: false,
                        processData: false,
                        type: 'POST',
                        success: (resp) => {
                            console.log('FILE SUBMITTED - ID=' + 'flaw_' + _id + ' FILE=' + flaw.pictureFile);
                        }
                    });
                }

                resolve(_id);
            }
        });
    });
}

function postEntry(entry, index) {
    return new Promise(function(resolve) {
        let deferredFlaws = [];
        entry.flawInformation.forEach((flaw) => {
            deferredFlaws.push(postFlaw(flaw));
        });
        $.when(...deferredFlaws).then(() => {
            let flaws = entry.flawInformation.map((i) => i._id);
            let formData = new FormData();
            formData.append('category', entry.category.data._id);
            formData.append('title', entry.title);
            formData.append('manufacturer', entry.manufacturer);
            formData.append('yearBuilt', entry.yearBuilt);
            formData.append('inspectionSigns', entry.inspectionSigns);
            formData.append('manufactureInfoAvailable', entry.manufactureInfoAvailable);
            formData.append('easyAccess', entry.easyAccess);
            formData.append('flaws', flaws);
            formData.append('index', index);

            $.ajax({
                type: 'POST',
                url: urlApi + 'entries/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                success: (resp) => {
                    let _id = resp.result._id;
                    console.log('ENTRY SUBMITTED - ID=' + _id);
                    entry._id = _id;

                    resolve(_id);
                }
            });
        });

    });
}

export function postProtocol(protocol) {
    return new Promise(function(resolve) {
        let deferredEntries = [];
        protocol.entries.forEach((item, index) => {
            let entry = item.data;
            deferredEntries.push(postEntry(entry, index))
        });

        $.when(...deferredEntries).then(() => {
            let entries = protocol.entries.map((i) => i.data._id);
            let formData = new FormData();
            let header = protocol.header;
            formData.append('title', header.title);
            formData.append('inspectionStandards', header.inspectionStandards);
            formData.append('inspectionDate', header.inspectionDate);
            formData.append('attendees', header.attendees);
            formData.append('facility', header.facility.data._id);
            formData.append('inspector', header.inspector.data._id);
            formData.append('issuer', header.issuer.data._id);
            formData.append('entries', entries);
            $.ajax({
                type: 'POST',
                url: urlApi + 'protocols/',
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
                success: (resp) => {
                    let _id = resp.result._id;
                    console.log('PROTOCOL SUBMITTED - ID=' + _id);

                    resolve(_id);
                }
            });
        });
    });
}