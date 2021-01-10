import {Component, Input, OnInit} from '@angular/core';
import {Job} from "../../models/models";
import {MatDialog} from "@angular/material/dialog";
import {
  ConfirmationDialogComponent,
  ConfirmDialogModel
} from "../../shared/confirmation-dialog/confirmation-dialog.component";
import {ScrapingService} from "../../services/scraping.service";

@Component({
  selector: 'jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit {

  result: string = '';


  @Input() data: Job[];
  @Input() typeState: string;

  pendingColumns: string[] = ['id', 'spider']
  runningColumns: string[] = ['id', 'spider', 'start_time', 'elapsed', 'action'];
  finishedColumns: string[] = ['id', 'spider', 'start_time', 'elapsed', 'end_time'];

  mapper = {
    'pending': this.pendingColumns,
    'running': this.runningColumns,
    'finished': this.finishedColumns
  }


  constructor(private service: ScrapingService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  getDataDiff(startDate: Date, endDate: Date) {
    let startTime = new Date(startDate).getTime();
    let _endTime = new Date();
    _endTime.setHours(_endTime.getHours() - 1);
    let endTime = _endTime.getTime();
    if (endDate) {
      endTime = new Date(endDate).getTime();
    }
    const diff = endTime - startTime;
    let days = Math.floor(diff / (60 * 60 * 24 * 1000));
    let hours = Math.floor(diff / (60 * 60 * 1000)) - (days * 24);
    let minutes = Math.floor(diff / (60 * 1000)) - ((days * 24 * 60) + (hours * 60));
    let seconds = Math.floor(diff / 1000) - ((days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60));
    return `${days}d ${hours}h ${minutes}m ${seconds}s`
  }


  confirmDialog(id: string): void {
    const message = `Czy na pewno chcesz zatrzymać zadanie #${id}?`;
    const dialogData = new ConfirmDialogModel("Anuluj zadanie", message);

    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: "500px",
      data: dialogData
    });

    dialogRef.afterClosed().subscribe(dialogResult => {
      this.result = dialogResult;
    });

    if (this.result) {
      this.service.cancelJob(id).subscribe((data) => {
        console.debug(`Cancel job #${id}`);
      })
    }
  }

}
