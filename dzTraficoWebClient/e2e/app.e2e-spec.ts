import { PrimeNgAppPage } from './app.po';

describe('prime-ng-app App', () => {
  let page: PrimeNgAppPage;

  beforeEach(() => {
    page = new PrimeNgAppPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
