/*(C) 2019 The Johns Hopkins University Applied Physics Laboratory LLC. */
import { Component, OnInit, AfterViewInit, ViewChild } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { ActivatedRoute } from "@angular/router";
import { Router } from "@angular/router";
import { HttpErrorResponse } from "@angular/common/http";

import { take } from "rxjs/operators";

import { PATHS } from "../../app.paths";

import { AuthService } from "../../service/auth/auth.service";
import { DocumentRepositoryService } from "../../service/document-repository/document-repository.service";
import { CollectionRepositoryService } from "../../service/collection-repository/collection-repository.service";
import { EventService } from "../../service/event/event.service";

import { Document } from "../../model/document";
import { CreatedObject } from "../../model/created";

import { ImageChooserComponent } from "../image-chooser/image-chooser.component";
import { uuidv4 } from "../util";

@Component({
    selector: "app-add-document",
    templateUrl: "./add-document.component.html",
    styleUrls: ["./add-document.component.css"]
})
export class AddDocumentComponent implements OnInit, AfterViewInit {

    public static readonly SUBTITLE = "Add Document to Collection";

    public readonly PATHS = PATHS;

    public readonly uuidv4 = uuidv4();

    public loading = false;
    public submitted = false;
    public hadError = false;
    public errorMessage: string;

    public createForm: FormGroup;
    public collection_id: string;

    @ViewChild(ImageChooserComponent)
    public imageChooser: ImageChooserComponent;

    constructor(private route: ActivatedRoute,
                private router: Router,
                private auth: AuthService,
                private event: EventService,
                private formBuilder: FormBuilder,
                private documentRepository: DocumentRepositoryService,
                private collectionRepository: CollectionRepositoryService) {
        this.createForm = this.formBuilder.group({
            creator_name: [{value: this.auth.loggedInUser.display_name, disabled: true},
                           [Validators.required]],
            creator_id: [{value: this.auth.loggedInUser.id, disabled: true},
                         [Validators.required]],
            collection_id: [{value: undefined, disabled: true},
                            [Validators.required]],
            text: ["", Validators.required]
        });
    }

    ngOnInit() {
        this.loading = true;
        this.route.paramMap.subscribe(params => {
            this.collection_id = params.get("collection_id");
            this.f.collection_id.setValue(this.collection_id);
            this.loading = false;
        });
    }

    ngAfterViewInit() {
        this.createForm.addControl("image", this.imageChooser.form);
        this.f.image.updateValueAndValidity();
    }

    // convenience getter for easy access to form fields
    get f() { return this.createForm.controls; }

    public handleFileInput(files: FileList) {
        const fileReader = new FileReader();
        fileReader.onload = (e) => {
            this.f.text.setValue(fileReader.result);
        };
        fileReader.readAsText(files[0]);
    }

    public create() {
        this.submitted = true;
        this.imageChooser.markAsTouched();
        
        if(this.createForm.invalid) {
            return;
        }

        const document = <Document>{};
        document.creator_id = this.f.creator_id.value;
        document.collection_id = this.f.collection_id.value;
        document.overlap = 0; // ???
        document.text = this.f.text.value;

        this.hadError = false;
        this.errorMessage = null;
        this.imageChooser.updateDocumentBeingCreated(document).pipe(take(1)).subscribe(_ => {
            console.log("Adding document");
            console.log(document);
            this.documentRepository.postDocument(document).subscribe(
                (createdDocument: CreatedObject) => {
                    const documentId = createdDocument._id;
                    this.event.showUserMessage.emit("Successfully added document with ID " + documentId);
                    this.event.documentAddedById.emit({collectionId: this.collection_id, documentId: documentId});
                    this.router.navigate([`/${PATHS.document.annotate}`, documentId]);
                }, (error: HttpErrorResponse) => {
                    console.error(error);
                    this.errorMessage = "Error: " + JSON.stringify(error["error"]);
                    this.hadError = true;
                }
            );
        }, (error) => {
            console.error(error);
            this.errorMessage = "Error uploading image: " + JSON.stringify(error["error"]);
            this.hadError = true;
        });
    }

}
