import { DzTraficoWebClientPage } from './app.po';

describe('dz-trafico-web-client App', () => {
  let page: DzTraficoWebClientPage;

  beforeEach(() => {
    page = new DzTraficoWebClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
