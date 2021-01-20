import {Component, HostListener} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'carApp';

  @HostListener('window:message', ['$event'])
  onMessage(event) {
    if (event.data == "FrameHeight") {
      let body = document.body;
      let html = document.documentElement;
      let height = Math.max(body.scrollHeight, body.offsetHeight,
        html.clientHeight, html.scrollHeight, html.offsetHeight);

      // send height back to parent page
      event.source.postMessage({"FrameHeight": height}, "*");
    }
  };

}
