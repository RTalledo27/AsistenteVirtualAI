import { TestBed } from '@angular/core/testing';

import { ConversacionesService } from './conversaciones.service';

describe('ConversacionesService', () => {
  let service: ConversacionesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConversacionesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
