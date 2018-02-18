import { urlApi } from './urls.js';
import { endpointByType, getRepr } from './helpers.js';

const $ = require('jquery');

function postFlaw(flaw) {
    return new Promise(function(resolve, reject) {
        let pictureType = flaw.pictureFile ? flaw.pictureFile.name.split('.').pop() : '';
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
            },
            error: reject
        });
    });
}

function postEntry(entry, index) {
    return new Promise(function(resolve, reject) {
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
                },
                error: reject
            });
        }, reject);
    });
}

export function postProtocol(protocol) {
    return new Promise(function(resolve, reject) {
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
                },
                error: reject
            });
        }, reject);
    });
}

export function fetch(endpoint, reprSelector, resultCallback, errorCallback) {
    $.ajax({
        type: 'GET',
        url: urlApi + endpoint,
        data: {},
        success: function(resp, status) {
            console.log('FETCHED ' + endpoint);
            console.log(JSON.stringify(resp));

            resultCallback(resp.result.map(function(i) { 
                return {
                    repr: reprSelector(i),
                    data: i
                };
            }));
        },
        error: errorCallback
    });
}

function getSimple(_id, type) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url : urlApi + endpointByType(type),
            data: { _id: _id },
            type: 'GET',
            success: (resp) => {
                let res = resp.result;
                resolve({
                    repr: getRepr(res, type),
                    data: res
                });
            },
            error: reject
        });
    });
}

export function getOrganization(_id) {
    return getSimple(_id, 'organization');
}

export function getInspectionStandard(_id) {
    return getSimple(_id, 'inspectionStandard');
}

export function getFacility(_id) {
    return getSimple(_id, 'facility');
}

export function getCategory(_id) {
    return new Promise((resolve, reject) => {
        getSimple(_id, 'category').then((result) => {
            let data = result.data;
            let deferredInspStds = data.inspectionStandards.split(',').map(getInspectionStandard);

            $.when(...deferredInspStds).then((results) => {
                console.log(results);
            }, reject);
        }, reject);
    });
}

export function getPerson(_id) {
    return new Promise((resolve, reject) => {
        getSimple(_id, 'person').then((person) => {
            getSimple(person.data.organization, 'organization').then((org) => {
                person.data.organization = org;
                resolve(person);
            }, reject);
        }, reject);
    });
}
